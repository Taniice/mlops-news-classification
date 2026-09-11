# -*- coding: utf-8 -*-
"""
src/ui_html.py
HTML, CSS, and JS template for the end-user interactive News Classifier UI.
"""

HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portal de Clasificación de Noticias con IA</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #0b132b;
      --card-bg: rgba(28, 37, 65, 0.75);
      --card-border: rgba(255, 255, 255, 0.1);
      --primary: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.35);
      --accent-purple: #c084fc;
      --accent-green: #4ade80;
      --accent-amber: #fbbf24;
      --accent-cyan: #22d3ee;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Inter', sans-serif;
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(at 10% 10%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
        radial-gradient(at 90% 90%, rgba(192, 132, 252, 0.15) 0px, transparent 50%);
      color: var(--text-main);
      min-height: 100vh;
      padding: 2.5rem 1rem;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .container { max-width: 1050px; width: 100%; }

    /* Header */
    header { text-align: center; margin-bottom: 2.5rem; }

    .badge-status {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.4rem 1rem;
      background: rgba(74, 222, 128, 0.12);
      border: 1px solid rgba(74, 222, 128, 0.35);
      border-radius: 9999px;
      color: var(--accent-green);
      font-size: 0.88rem;
      font-weight: 600;
      margin-bottom: 1.25rem;
    }

    .dot-pulse {
      width: 9px;
      height: 9px;
      background-color: var(--accent-green);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--accent-green);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.25); }
    }

    h1 {
      font-family: 'Outfit', sans-serif;
      font-size: 2.75rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.6rem;
    }

    p.subtitle {
      color: var(--text-muted);
      font-size: 1.1rem;
      max-width: 650px;
      margin: 0 auto;
    }

    /* Layout Grid */
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.75rem;
    }

    @media (max-width: 850px) { .grid { grid-template-columns: 1fr; } }

    /* Glass Card */
    .glass-card {
      background: var(--card-bg);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--card-border);
      border-radius: 1.5rem;
      padding: 1.85rem;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
      transition: all 0.3s ease;
    }

    .glass-card:hover { border-color: rgba(255, 255, 255, 0.18); }

    .card-title {
      font-family: 'Outfit', sans-serif;
      font-size: 1.3rem;
      font-weight: 700;
      margin-bottom: 1.2rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    /* Preset Buttons */
    .presets-label {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 0.6rem;
      font-weight: 500;
    }

    .presets-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.6rem;
      margin-bottom: 1.25rem;
    }

    .btn-preset {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 0.65rem 0.85rem;
      border-radius: 0.75rem;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
    }

    .btn-preset:hover {
      background: rgba(56, 189, 248, 0.12);
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-2px);
    }

    /* Textarea Area */
    textarea {
      width: 100%;
      height: 150px;
      background: rgba(11, 19, 43, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 0.85rem;
      padding: 1rem;
      color: #ffffff;
      font-family: 'Inter', sans-serif;
      font-size: 0.98rem;
      line-height: 1.5;
      resize: vertical;
      outline: none;
      transition: all 0.2s ease;
    }

    textarea:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-glow);
    }

    .action-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 0.5rem;
      margin-bottom: 1.25rem;
    }

    .btn-clear {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 0.85rem;
      cursor: pointer;
      text-decoration: underline;
    }

    .btn-clear:hover { color: #ffffff; }

    .char-counter { font-size: 0.82rem; color: var(--text-muted); }

    /* Primary Action Button */
    .btn-submit {
      width: 100%;
      padding: 1rem;
      background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
      border: none;
      border-radius: 0.85rem;
      color: #ffffff;
      font-family: 'Outfit', sans-serif;
      font-size: 1.1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 10px 25px rgba(2, 132, 199, 0.35);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.6rem;
    }

    .btn-submit:hover {
      transform: translateY(-2px);
      box-shadow: 0 15px 30px rgba(2, 132, 199, 0.5);
    }

    /* Output Results Placeholder */
    .result-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 300px;
      color: var(--text-muted);
      text-align: center;
      border: 2px dashed rgba(255, 255, 255, 0.08);
      border-radius: 0.85rem;
      padding: 2rem;
    }

    .result-placeholder svg {
      width: 52px;
      height: 52px;
      margin-bottom: 1rem;
      opacity: 0.35;
    }

    .result-content { display: none; }

    /* Category Main Card */
    .category-hero {
      padding: 1.35rem;
      border-radius: 1rem;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      margin-bottom: 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .cat-info { display: flex; align-items: center; gap: 0.85rem; }
    .cat-icon { font-size: 2.4rem; }
    .cat-name { font-family: 'Outfit', sans-serif; font-size: 1.45rem; font-weight: 700; }
    .cat-subtitle { font-size: 0.82rem; color: var(--text-muted); }

    .conf-badge { text-align: right; }
    .conf-score { font-family: 'Outfit', sans-serif; font-size: 1.75rem; font-weight: 800; }
    .conf-label { font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }

    /* Probabilities Section */
    .prob-section-title {
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .prob-item { margin-bottom: 0.9rem; }
    .prob-header { display: flex; justify-content: space-between; font-size: 0.92rem; margin-bottom: 0.35rem; font-weight: 500; }

    .bar-bg {
      width: 100%;
      height: 9px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 9999px;
      overflow: hidden;
    }

    .bar-fill {
      height: 100%;
      border-radius: 9999px;
      width: 0%;
      transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Feedback & Copy Toolbar */
    .user-tools {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1.25rem;
      padding-top: 1rem;
      border-top: 1px solid var(--card-border);
    }

    .feedback-buttons { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: var(--text-muted); }

    .btn-feedback {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 0.4rem 0.65rem;
      border-radius: 0.5rem;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.2s ease;
    }

    .btn-feedback:hover { background: rgba(255, 255, 255, 0.15); }

    .btn-copy {
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: var(--primary);
      padding: 0.45rem 0.85rem;
      border-radius: 0.6rem;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-copy:hover { background: rgba(56, 189, 248, 0.25); }

    /* Category Specific Color Themes */
    .theme-world { background: rgba(192, 132, 252, 0.12); border-color: rgba(192, 132, 252, 0.35); }
    .theme-world .conf-score, .theme-world .cat-name { color: var(--accent-purple); }
    .theme-world .bar-fill { background: linear-gradient(90deg, #c084fc, #a855f7); }

    .theme-sports { background: rgba(251, 191, 36, 0.12); border-color: rgba(251, 191, 36, 0.35); }
    .theme-sports .conf-score, .theme-sports .cat-name { color: var(--accent-amber); }
    .theme-sports .bar-fill { background: linear-gradient(90deg, #fbbf24, #d97706); }

    .theme-business { background: rgba(74, 222, 128, 0.12); border-color: rgba(74, 222, 128, 0.35); }
    .theme-business .conf-score, .theme-business .cat-name { color: var(--accent-green); }
    .theme-business .bar-fill { background: linear-gradient(90deg, #4ade80, #16a34a); }

    .theme-scitech { background: rgba(34, 211, 238, 0.12); border-color: rgba(34, 211, 238, 0.35); }
    .theme-scitech .conf-score, .theme-scitech .cat-name { color: var(--accent-cyan); }
    .theme-scitech .bar-fill { background: linear-gradient(90deg, #22d3ee, #0284c7); }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: #1e293b;
      color: #ffffff;
      border: 1px solid var(--accent-green);
      padding: 0.85rem 1.25rem;
      border-radius: 0.75rem;
      font-size: 0.9rem;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      display: none;
      animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    .spinner {
      width: 22px; height: 22px;
      border: 3px solid rgba(255, 255, 255, 0.3);
      border-top-color: #ffffff;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      display: none;
    }

    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div class="container">
    
    <!-- Header -->
    <header>
      <div class="badge-status">
        <div class="dot-pulse"></div>
        <span>Sistema de Inteligencia Artificial Activo</span>
      </div>
      <h1>Clasificador Inteligente de Noticias</h1>
      <p class="subtitle">Escribe o pega cualquier noticia en español o inglés para analizar su tema al instante.</p>
    </header>

    <!-- Main Grid -->
    <div class="grid">
      
      <!-- Input Card -->
      <div class="glass-card">
        <div class="card-title">
          <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
          Noticia a Analizar
        </div>

        <div class="presets-label">Prueba con ejemplos rápidos:</div>
        <div class="presets-grid">
          <button class="btn-preset" onclick="setPreset('world')">🌐 <span>Mundo</span></button>
          <button class="btn-preset" onclick="setPreset('sports')">⚽ <span>Deportes</span></button>
          <button class="btn-preset" onclick="setPreset('business')">📈 <span>Economía</span></button>
          <button class="btn-preset" onclick="setPreset('scitech')">💻 <span>Tecnología</span></button>
        </div>

        <textarea id="newsText" placeholder="Pega o escribe aquí el texto o titular de la noticia..."></textarea>
        
        <div class="action-bar">
          <button class="btn-clear" onclick="clearText()">Borrar texto</button>
          <div class="char-counter"><span id="charCount">0</span> caracteres</div>
        </div>

        <button class="btn-submit" id="btnSubmit" onclick="classifyNews()">
          <div class="spinner" id="spinner"></div>
          <span id="btnText">✨ Clasificar Noticia</span>
        </button>
      </div>

      <!-- Result Card -->
      <div class="glass-card">
        <div class="card-title">
          <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Resultado del Análisis
        </div>

        <!-- Initial Placeholder -->
        <div class="result-placeholder" id="placeholder">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>
          <p>El análisis de la noticia aparecerá aquí de forma automática al presionar el botón.</p>
        </div>

        <!-- Actual Output Content -->
        <div class="result-content" id="resultContent">
          
          <div class="category-hero" id="categoryHero">
            <div class="cat-info">
              <div class="cat-icon" id="catIcon">💻</div>
              <div>
                <div class="cat-name" id="catName">Tecnología y Ciencia</div>
                <div class="cat-subtitle" id="catSub">Categoría Principal Detectada</div>
              </div>
            </div>
            <div class="conf-badge">
              <div class="conf-score" id="confScore">95.4%</div>
              <div class="conf-label">Precisión</div>
            </div>
          </div>

          <div class="prob-section-title">Probabilidad por Categorías</div>
          <div id="probBarsContainer"></div>

          <div class="user-tools">
            <div class="feedback-buttons">
              <span>¿Es correcta esta categoría?</span>
              <button class="btn-feedback" onclick="sendFeedback(true)">👍</button>
              <button class="btn-feedback" onclick="sendFeedback(false)">👎</button>
            </div>
            <button class="btn-copy" onclick="copyResult()">📋 Copiar Resultado</button>
          </div>

        </div>
      </div>

    </div>
  </div>

  <div class="toast" id="toast"></div>

  <script>
    const PRESETS = {
      world: "Líderes de diversos países se reúnen en la Cumbre Internacional de Ginebra para firmar un tratado histórico de paz y diplomacia.",
      sports: "El Real Madrid asegura la victoria en la final de la Champions League tras anotar dos goles decisivos en el tiempo reglamentario.",
      business: "Las acciones de la bolsa de valores alcanzan máximos históricos luego de que el Banco Central anunciara una baja en las tasas de interés.",
      scitech: "OpenAI y Microsoft presentan un nuevo avance revolucionario en Inteligencia Artificial capaz de procesar texto y código al instante."
    };

    const ICON_MAP = {
      "Mundo": "🌐", "Global": "🌐",
      "Deportes": "⚽",
      "Economía": "📈", "Negocios": "📈",
      "Tecnología": "💻", "Ciencia": "💻"
    };

    const THEME_MAP = {
      "Mundo": "theme-world", "Global": "theme-world",
      "Deportes": "theme-sports",
      "Economía": "theme-business", "Negocios": "theme-business",
      "Tecnología": "theme-scitech", "Ciencia": "theme-scitech"
    };

    const txtArea = document.getElementById("newsText");
    const charCount = document.getElementById("charCount");
    let lastResult = "";

    txtArea.addEventListener("input", () => {
      charCount.textContent = txtArea.value.length;
    });

    function setPreset(key) {
      txtArea.value = PRESETS[key];
      charCount.textContent = txtArea.value.length;
    }

    function clearText() {
      txtArea.value = "";
      charCount.textContent = 0;
    }

    function showToast(msg) {
      const toast = document.getElementById("toast");
      toast.textContent = msg;
      toast.style.display = "block";
      setTimeout(() => { toast.style.display = "none"; }, 2500);
    }

    async function classifyNews() {
      const text = txtArea.value.trim();
      if (!text) {
        showToast("⚠️ Escribe o pega una noticia primero.");
        return;
      }

      const btn = document.getElementById("btnSubmit");
      const spinner = document.getElementById("spinner");
      const btnText = document.getElementById("btnText");

      spinner.style.display = "block";
      btnText.textContent = "Analizando Noticia...";
      btn.disabled = true;

      try {
        const response = await fetch("/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: text, top_k: 4 })
        });

        if (!response.ok) throw new Error("Error en la conexión.");

        const data = await response.json();
        displayResults(data);

      } catch (err) {
        showToast("❌ Error al procesar noticia: " + err.message);
      } finally {
        spinner.style.display = "none";
        btnText.textContent = "✨ Clasificar Noticia";
        btn.disabled = false;
      }
    }

    function displayResults(data) {
      document.getElementById("placeholder").style.display = "none";
      document.getElementById("resultContent").style.display = "block";

      const hero = document.getElementById("categoryHero");
      const label = data.label;
      lastResult = `Noticia: "${txtArea.value.substring(0, 50)}..." -> Categoría: ${label} (${(data.confidence * 100).toFixed(1)}% precisión)`;

      let matchedTheme = "theme-scitech";
      let matchedIcon = "💻";

      for (const k in THEME_MAP) {
        if (label.includes(k)) {
          matchedTheme = THEME_MAP[k];
          matchedIcon = ICON_MAP[k];
          break;
        }
      }

      hero.className = "category-hero " + matchedTheme;
      document.getElementById("catIcon").textContent = matchedIcon;
      document.getElementById("catName").textContent = label;
      document.getElementById("confScore").textContent = (data.confidence * 100).toFixed(1) + "%";

      const container = document.getElementById("probBarsContainer");
      container.innerHTML = "";

      data.top_predictions.forEach(item => {
        const pct = (item.probability * 100).toFixed(1);
        
        let themeClass = "theme-scitech";
        for (const k in THEME_MAP) {
          if (item.label.includes(k)) {
            themeClass = THEME_MAP[k];
            break;
          }
        }

        const div = document.createElement("div");
        div.className = "prob-item " + themeClass;
        div.innerHTML = `
          <div class="prob-header">
            <span>${item.label}</span>
            <span><strong>${pct}%</strong></span>
          </div>
          <div class="bar-bg">
            <div class="bar-fill" style="width: 0%"></div>
          </div>
        `;
        container.appendChild(div);

        setTimeout(() => {
          div.querySelector(".bar-fill").style.width = pct + "%";
        }, 50);
      });
    }

    function copyResult() {
      if (!lastResult) return;
      navigator.clipboard.writeText(lastResult);
      showToast("📋 Resultado copiado al portapapeles.");
    }

    function sendFeedback(isPositive) {
      if (isPositive) {
        showToast("👍 ¡Gracias por tu confirmación!");
      } else {
        showToast("💡 Gracias por tus comentarios para mejorar el modelo.");
      }
    }
  </script>
</body>
</html>
"""
