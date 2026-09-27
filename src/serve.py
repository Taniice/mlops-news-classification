"""
src/serve.py
────────────
FastAPI model server for the news classifier.

Endpoints:
  POST /predict       — text → label + confidence
  GET  /model/info    — current model version & metrics
  GET  /health        — health check

Run:
  uvicorn src.serve:app --host 0.0.0.0 --port 8000 --reload
  OR
  python src/serve.py
"""

import json
import logging
import os
import time
import yaml
import joblib
import numpy as np

import re
import urllib.request
from html import unescape
from pathlib import Path
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from src.ui_html import HTML_CONTENT

log = logging.getLogger("uvicorn.error")

ROOT   = Path(__file__).resolve().parent.parent
PARAMS = yaml.safe_load(open(ROOT / "params.yaml"))

# ══════════════════════════════════════════════════════════════════════════════
# ⚙️ CONFIGURACIÓN DE LÍMITE DE CONSULTAS / TOKEN RATE LIMIT
# Modifica estas dos variables para ajustar la cuota de preguntas y el tiempo:
# ══════════════════════════════════════════════════════════════════════════════
TOKEN_MAX_QUESTIONS = 20    # <- LÍNEA 47: Cantidad máxima de preguntas por ciclo
TOKEN_RESET_MINUTES = 5     # <- LÍNEA 48: Minutos tras los cuales se reactiva el token
# ══════════════════════════════════════════════════════════════════════════════

# Almacén en memoria de cuotas por IP/cliente: { client_ip: {"remaining": int, "reset_time": float} }
TOKEN_STORE = {}

def get_client_ip(req: Request) -> str:
    """Extrae la IP real del cliente considerando proxies o peticiones directas."""
    forwarded = req.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return req.client.host if req.client else "127.0.0.1"

def check_and_consume_token(client_ip: str) -> tuple:
    """
    Verifica si el cliente tiene tokens disponibles y descuenta 1.
    El período de espera de 5 minutos SOLO comienza cuando los tokens se agotan por completo (llegan a 0).
    Retorna (permitido: bool, restantes: int, segundos_para_reactivacion: int).
    """
    now = time.time()
    reset_window = TOKEN_RESET_MINUTES * 60

    if client_ip not in TOKEN_STORE:
        TOKEN_STORE[client_ip] = {
            "remaining": TOKEN_MAX_QUESTIONS,
            "reset_time": None
        }

    data = TOKEN_STORE[client_ip]

    # Si se habían agotado y ya pasaron los 5 minutos, reactivar 20 tokens de nuevo
    if data["remaining"] <= 0 and data["reset_time"] is not None:
        if now >= data["reset_time"]:
            data["remaining"] = TOKEN_MAX_QUESTIONS
            data["reset_time"] = None

    # Si aún no le quedan tokens (sigue en el periodo de 5 minutos de espera)
    if data["remaining"] <= 0:
        reset_seconds = max(0, int(data["reset_time"] - now)) if data["reset_time"] else int(reset_window)
        return False, 0, reset_seconds

    # Consumir un token
    data["remaining"] -= 1

    # Si este fue el último token disponible (llegó a 0), iniciar el conteo de 5 minutos para reactivar
    if data["remaining"] == 0:
        data["reset_time"] = now + reset_window
        reset_seconds = int(reset_window)
    else:
        data["reset_time"] = None
        reset_seconds = 0

    return True, data["remaining"], reset_seconds

def get_token_status(client_ip: str) -> dict:
    """Obtiene el estado actual de los tokens del cliente."""
    now = time.time()
    reset_window = TOKEN_RESET_MINUTES * 60

    if client_ip not in TOKEN_STORE:
        TOKEN_STORE[client_ip] = {
            "remaining": TOKEN_MAX_QUESTIONS,
            "reset_time": None
        }

    data = TOKEN_STORE[client_ip]

    # Si estaban en 0 y ya pasaron los 5 minutos, reactivar automáticamente
    if data["remaining"] <= 0 and data["reset_time"] is not None:
        if now >= data["reset_time"]:
            data["remaining"] = TOKEN_MAX_QUESTIONS
            data["reset_time"] = None

    reset_seconds = max(0, int(data["reset_time"] - now)) if data.get("reset_time") else 0
    return {
        "max_questions": TOKEN_MAX_QUESTIONS,
        "remaining": data["remaining"],
        "reset_seconds": reset_seconds,
        "reset_minutes": TOKEN_RESET_MINUTES,
        "is_exhausted": data["remaining"] <= 0
    }

# ── Global state ──────────────────────────────────────────────────────────────
MODEL_STATE = {
    "pipeline"     : None,
    "model_version": "unknown",
    "label_names"  : [],
    "metrics"      : {},
    "loaded_at"    : None,
}


# ──────────────────────────────────────────────────────────────────────────────
# Model loading
# ──────────────────────────────────────────────────────────────────────────────

def _load_model():
    """Try MLflow Registry first, fall back to local pkl."""
    import mlflow
    import mlflow.sklearn

    tracking_uri = PARAMS["mlflow"]["tracking_uri"]
    model_name   = PARAMS["mlflow"]["registered_model_name"]
    stage        = PARAMS["serving"]["model_stage"]

    mlflow.set_tracking_uri(tracking_uri)

    try:
        model_uri = f"models:/{model_name}/{stage}"
        pipeline  = mlflow.sklearn.load_model(model_uri)

        # Fetch version metadata
        client = mlflow.MlflowClient()
        versions = client.get_latest_versions(model_name, stages=[stage])
        version  = versions[0].version if versions else "unknown"
        run_id   = versions[0].run_id  if versions else None

        metrics = {}
        if run_id:
            run  = client.get_run(run_id)
            metrics = {k: round(v, 4) for k, v in run.data.metrics.items()}

        MODEL_STATE.update({
            "pipeline"     : pipeline,
            "model_version": version,
            "metrics"      : metrics,
            "loaded_at"    : time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        log.info(f"✅  Loaded model '{model_name}' v{version} from MLflow ({stage})")

    except Exception as e:
        log.warning(f"MLflow load failed ({e}), falling back to local pkl …")

        pkls = sorted((ROOT / "models").glob("*.pkl"))
        if not pkls:
            raise RuntimeError("No model found — run src/train.py first")

        pipeline = joblib.load(pkls[-1])
        MODEL_STATE.update({
            "pipeline"     : pipeline,
            "model_version": f"local:{pkls[-1].stem}",
            "metrics"      : {},
            "loaded_at"    : time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        log.info(f"✅  Loaded local model: {pkls[-1]}")

    LABEL_MAP = {
        0: "Mundo y Política Global",
        1: "Deportes",
        2: "Economía y Negocios",
        3: "Tecnología y Ciencia",
    }
    try:
        raw_classes = MODEL_STATE["pipeline"].classes_
        MODEL_STATE["label_names"] = [
            LABEL_MAP.get(int(c), str(c)) for c in raw_classes
        ]
    except Exception:
        MODEL_STATE["label_names"] = [LABEL_MAP.get(i, str(i)) for i in range(4)]


def _extract_text_from_url(url: str) -> str:
    """Fetch web page content from URL link and extract article title and paragraphs."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode("utf-8", errors="ignore")
        
        # Extract title tag
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1) if title_match else ""

        # Extract paragraph tags
        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", html, re.IGNORECASE | re.DOTALL)
        clean_p = [re.sub(r"<[^>]+>", "", p).strip() for p in paragraphs]
        text_content = " ".join([title] + [p for p in clean_p if len(p) > 20])
        clean_text = unescape(re.sub(r"\s+", " ", text_content)).strip()

        if len(clean_text) > 30:
            log.info(f"✅ Extracted {len(clean_text)} chars from URL: {url}")
            return clean_text[:4000]
    except Exception as e:
        log.warning(f"Failed to fetch content from URL {url}: {e}")
    return url


def _preprocess_user_text(text: str) -> str:
    """Helper to handle URL links and enrich Spanish text with domain keywords."""
    clean_input = text.strip()
    if clean_input.startswith(("http://", "https://")):
        clean_input = _extract_text_from_url(clean_input)

    text_lower = clean_input.lower()
    spanish_keywords = {
        "deportes": ["fútbol", "futbol", "gol", "partido", "liga", "champions", "copa", "baloncesto", "tenis", "jugador", "campeón", "campeon", "equipo", "marcador", "victoria"],
        "sports_enrich": "sports match team player league goal championship tournament victory cup",
        
        "economia": ["banco", "interés", "interes", "bolsa", "acciones", "mercado", "empresa", "economía", "economia", "finanzas", "inflación", "inflacion", "dólares", "dolares", "inversión", "inversion", "ganancias", "precio"],
        "econ_enrich": "business economy finance market stock company bank interest investment profit price",
        
        "tecnologia": ["tecnología", "tecnologia", "inteligencia artificial", "software", "app", "chip", "computadora", "ordenador", "celular", "teléfono", "internet", "nasa", "ciencia", "robot", "espacio", "satélite", "ia"],
        "tech_enrich": "technology science artificial intelligence software app chip computer phone internet space robot nasa",

        "mundo": ["presidente", "gobierno", "acuerdo", "tratado", "guerra", "paz", "cumbre", "elecciones", "países", "paises", "diplomacia", "onu", "naciones"],
        "world_enrich": "world government president treaty war peace summit elections diplomacy nations international"
    }

    enrichments = []
    if any(k in text_lower for k in spanish_keywords["deportes"]):
        enrichments.append(spanish_keywords["sports_enrich"])
    if any(k in text_lower for k in spanish_keywords["economia"]):
        enrichments.append(spanish_keywords["econ_enrich"])
    if any(k in text_lower for k in spanish_keywords["tecnologia"]):
        enrichments.append(spanish_keywords["tech_enrich"])
    if any(k in text_lower for k in spanish_keywords["mundo"]):
        enrichments.append(spanish_keywords["world_enrich"])

    if enrichments:
        return f"{clean_input} {' '.join(enrichments)}"
    return clean_input


# ──────────────────────────────────────────────────────────────────────────────
# App startup / shutdown
# ──────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_model()
    yield


app = FastAPI(
    title       = "News Classifier API — MLOps Pipeline",
    description = "Serves a TF-IDF + LR text classification model logged with MLflow.",
    version     = "1.0.0",
    lifespan    = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins  = ["*"],
    allow_methods  = ["*"],
    allow_headers  = ["*"],
)


# ──────────────────────────────────────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    text: str
    top_k: Optional[int] = 3          # return top-k class probabilities

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("text field must not be empty")
        return v.strip()


class PredictResponse(BaseModel):
    label: str
    label_id: int
    confidence: float
    top_predictions: List[dict]
    model_version: str
    latency_ms: float
    tokens_remaining: Optional[int] = None
    reset_seconds: Optional[int] = None


# ──────────────────────────────────────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui():
    """Serves the interactive web dashboard."""
    return HTMLResponse(content=HTML_CONTENT)


@app.get("/health", tags=["System"])
async def health():
    """Simple health check."""
    pipeline = MODEL_STATE["pipeline"]
    return {
        "status" : "healthy" if pipeline is not None else "model_not_loaded",
        "model_version": MODEL_STATE["model_version"],
        "loaded_at"    : MODEL_STATE["loaded_at"],
    }


@app.get("/token/status", tags=["System"])
async def token_status(raw_request: Request):
    """Consulta cuántas preguntas le quedan al usuario y en cuántos segundos se reactiva el token."""
    client_ip = get_client_ip(raw_request)
    return get_token_status(client_ip)


@app.get("/model/info", tags=["System"])
async def model_info():
    """Returns model version, metrics, and label mapping."""
    if MODEL_STATE["pipeline"] is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "model_name"   : PARAMS["mlflow"]["registered_model_name"],
        "model_version": MODEL_STATE["model_version"],
        "label_names"  : MODEL_STATE["label_names"],
        "metrics"      : MODEL_STATE["metrics"],
        "loaded_at"    : MODEL_STATE["loaded_at"],
        "tracking_uri" : PARAMS["mlflow"]["tracking_uri"],
    }


@app.post("/predict", response_model=PredictResponse, tags=["Inference"])
async def predict(request: PredictRequest, raw_request: Request):
    """
    Predict news category from text.

    Returns the predicted label, confidence, top-k probabilities, and remaining query tokens.
    """
    pipeline = MODEL_STATE["pipeline"]
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # ── Validación de Cuota / Token (20 preguntas / 5 minutos) ────────────────
    client_ip = get_client_ip(raw_request)
    allowed, remaining, reset_seconds = check_and_consume_token(client_ip)
    if not allowed:
        mins = reset_seconds // 60
        secs = reset_seconds % 60
        time_str = f"{mins:02d}:{secs:02d}"
        raise HTTPException(
            status_code=429,
            detail=f"Has alcanzado el límite de {TOKEN_MAX_QUESTIONS} preguntas. Tus tokens se reactivarán automáticamente pasados 5 minutos ({time_str} restantes).",
        )

    t0 = time.perf_counter()

    try:
        processed_text = _preprocess_user_text(request.text)
        proba          = pipeline.predict_proba([processed_text])[0]
        label_id       = int(np.argmax(proba))
        label          = MODEL_STATE["label_names"][label_id]
        confidence     = float(proba[label_id])

        top_k = min(request.top_k, len(MODEL_STATE["label_names"]))
        top_indices = np.argsort(proba)[::-1][:top_k]
        top_predictions = [
            {"label": MODEL_STATE["label_names"][i], "probability": round(float(proba[i]), 4)}
            for i in top_indices
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    latency_ms = (time.perf_counter() - t0) * 1000

    return PredictResponse(
        label           = label,
        label_id        = label_id,
        confidence      = round(confidence, 4),
        top_predictions = top_predictions,
        model_version   = MODEL_STATE["model_version"],
        latency_ms      = round(latency_ms, 2),
        tokens_remaining= remaining,
        reset_seconds   = reset_seconds,
    )


@app.post("/predict/batch", tags=["Inference"])
async def predict_batch(texts: List[str]):
    """Batch predict for multiple texts."""
    pipeline = MODEL_STATE["pipeline"]
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if len(texts) > 100:
        raise HTTPException(status_code=400, detail="Max batch size is 100")

    t0 = time.perf_counter()
    probas   = pipeline.predict_proba(texts)
    labels   = pipeline.predict(texts)
    latency  = (time.perf_counter() - t0) * 1000

    results = []
    for i, (label_id, proba) in enumerate(zip(labels, probas)):
        results.append({
            "text"      : texts[i][:100] + "…" if len(texts[i]) > 100 else texts[i],
            "label"     : MODEL_STATE["label_names"][int(label_id)],
            "confidence": round(float(proba[int(label_id)]), 4),
        })

    return {"predictions": results, "count": len(results), "latency_ms": round(latency, 2)}


@app.post("/model/reload", tags=["System"])
async def reload_model():
    """Hot-reload the Production model from MLflow Registry."""
    try:
        _load_model()
        return {"status": "reloaded", "model_version": MODEL_STATE["model_version"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────────────────────────────────────
# Run directly
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.serve:app",
        host    = PARAMS["serving"]["host"],
        port    = PARAMS["serving"]["port"],
        reload  = False,
        workers = 1,
    )
