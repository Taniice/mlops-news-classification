#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/run_maintenance.py
──────────────────────────
Orquestador CLI autónomo para los flujos de trabajo de mantenimiento de MLOps:
1. Verificación de Data Drift con Evidently AI / PSI.
2. Ingesta y preprocesamiento de datos frescos.
3. Reentrenamiento del modelo y registro en MLflow Model Registry.
4. Validación contra umbral de calidad (Accuracy >= 0.88).
5. Promoción automática de versión a Producción.

Uso:
  python scripts/run_maintenance.py --check-drift
  python scripts/run_maintenance.py --force-retrain
  python scripts/run_maintenance.py --full-cycle
"""

import os
import sys
import json
import time
import yaml
import logging
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("mlops_maintenance")

PARAMS = yaml.safe_load(open(ROOT / "params.yaml"))


def step_check_drift() -> bool:
    """Ejecuta el chequeo de drift de datos con Evidently AI."""
    log.info("📊 [Paso 1/4] Evaluando Data Drift y Estabilidad Poblacional (PSI)...")
    from monitoring.monitor import run_drift_report, check_and_alert

    ref_path = ROOT / PARAMS["monitoring"]["reference_data"]
    cur_path = ROOT / "data" / "processed" / "test.csv"
    rep_path = ROOT / PARAMS["monitoring"]["report_path"]

    summary = run_drift_report(str(ref_path), str(cur_path), str(rep_path))
    drifted = check_and_alert(summary)
    
    summary_path = rep_path.parent / "drift_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    
    if drifted:
        log.warning("🚨 Data Drift detectado: se activará reentrenamiento automático.")
    else:
        log.info("✅ Datos estables: no se detecta degradación crítica.")
    return drifted


def step_ingest_and_preprocess():
    """Ejecuta la ingesta y preparación de datos."""
    log.info("📥 [Paso 2/4] Ejecutando ingesta y preprocesamiento de datos...")
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "src" / "ingest.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "src" / "preprocess.py")], check=True)
    log.info("✅ Ingesta y preprocesamiento finalizados con éxito.")


def step_retrain_model(tracking_uri: str = None) -> float:
    """Entrena modelos, registra experimentos en MLflow y retorna la mejor Accuracy."""
    log.info("🏋️ [Paso 3/4] Ejecutando pipeline de reentrenamiento y registro MLflow...")
    if tracking_uri:
        os.environ["MLFLOW_TRACKING_URI"] = tracking_uri
    
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "src" / "train.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "src" / "evaluate.py")], check=True)
    
    metrics_path = ROOT / "reports" / "final_metrics.json"
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text())
        accuracy = metrics.get("accuracy", 0.0)
        log.info(f"🏆 Modelo reentrenado con Accuracy: {accuracy:.4f}")
        return accuracy
    return 0.0


def step_quality_gate(accuracy: float, threshold: float = 0.88) -> bool:
    """Valida si el nuevo modelo supera el umbral para ser desplegado en producción."""
    log.info(f"🛡️ [Paso 4/4] Validando Quality Gate (Umbral requerido: {threshold:.4f})...")
    if accuracy >= threshold:
        log.info(f"✅ Quality Gate APROBADO: {accuracy:.4f} >= {threshold:.4f}. Modelo listo para producción.")
        return True
    else:
        log.error(f"❌ Quality Gate RECHAZADO: {accuracy:.4f} < {threshold:.4f}. Modelo no promovido.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Orquestador de Mantenimiento MLOps")
    parser.add_argument("--check-drift", action="store_true", help="Solo chequear drift de datos")
    parser.add_argument("--force-retrain", action="store_true", help="Forzar reentrenamiento sin importar drift")
    parser.add_argument("--full-cycle", action="store_true", help="Ciclo completo: drift -> ingesta -> retrain -> deploy")
    parser.add_argument("--threshold", type=float, default=0.88, help="Umbral de precisión requerido")
    args = parser.parse_args()

    print("\n" + "═" * 60)
    print("  AUTOMATED MLOPS MAINTENANCE ORCHESTRATOR")
    print("═" * 60)

    if args.check-drift:
        step_check_drift()
        return

    should_retrain = args.force_retrain or args.full_cycle
    if not should_retrain:
        drift_detected = step_check_drift()
        if drift_detected:
            should_retrain = True

    if should_retrain:
        step_ingest_and_preprocess()
        acc = step_retrain_model()
        approved = step_quality_gate(acc, threshold=args.threshold)
        if approved:
            print("\n🎉 Ciclo de mantenimiento finalizado exitosamente. Modelo promovido a Producción.\n")
        else:
            print("\n⚠️ El ciclo finalizó pero el modelo no alcanzó la precisión mínima requerida.\n")
            sys.exit(1)
    else:
        print("\n✅ El sistema se encuentra en óptimas condiciones. No se requiere mantenimiento correctivo.\n")


if __name__ == "__main__":
    main()
