# -*- coding: utf-8 -*-
"""
src/ui_html.py
Plantilla HTML, CSS y JavaScript para la interfaz interactiva de clasificación de noticias.
100% en Español, con indicador claro de tokens y sin temporizador permanente.
Los 20 tokens se reactivan automáticamente pasados 5 minutos tras agotarse.
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
      --accent-red: #ef4444;
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

    .header-badges {
      display: flex;
      justify-content: center;
      gap: 0.75rem;
      flex-wrap: wrap;
      margin-bottom: 1.25rem;
    }

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
    }

    .badge-token-header {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.4rem 1rem;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 9999px;
      color: var(--accent-cyan);
      font-size: 0.88rem;
      font-weight: 600;
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
      margin-bottom: 1.1rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    /* Widget de Tokens (Sin reloj continuo) */
    .token-widget {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 1rem;
      padding: 0.9rem 1.15rem;
      margin-bottom: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
      transition: all 0.3s ease;
    }
    .token-widget.low {
      border-color: rgba(251, 191, 36, 0.55);
      background: rgba(45, 28, 12, 0.75);
    }
    .token-widget.empty {
      border-color: rgba(239, 68, 68, 0.7);
      background: rgba(50, 15, 20, 0.85);
    }
    .token-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.92rem;
    }
    .token-info {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 600;
    }
    .token-badge {
      color: var(--primary);
      font-weight: 700;
      background: rgba(56, 189, 248, 0.15);
      padding: 0.2rem 0.65rem;
      border-radius: 999px;
      border: 1px solid rgba(56, 189, 248, 0.35);
      letter-spacing: 0.02em;
    }
    .token-widget.low .token-badge {
      color: var(--accent-amber);
      background: rgba(251, 191, 36, 0.18);
      border-color: rgba(251, 191, 36, 0.35);
    }
    .token-widget.empty .token-badge {
      color: #ef4444;
      background: rgba(239, 68, 68, 0.2);
      border-color: rgba(239, 68, 68, 0.4);
    }
    .token-status-text {
      font-size: 0.82rem;
      color: var(--accent-green);
      font-weight: 600;
    }
    .token-widget.empty .token-status-text {
      color: var(--accent-red);
    }
    .token-progress-bg {
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 999px;
      overflow: hidden;
    }
    .token-progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      border-radius: 999px;
      transition: width 0.4s ease, background 0.4s ease;
    }
    .token-widget.low .token-progress-fill {
      background: linear-gradient(90deg, #fbbf24, #f59e0b);
    }
    .token-widget.empty .token-progress-fill {
      background: linear-gradient(90deg, #ef4444, #b91c1c);
    }
    .token-alert-banner {
      display: none;
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid rgba(239, 68, 68, 0.5);
      color: #fca5a5;
      padding: 0.65rem 0.9rem;
      border-radius: 0.6rem;
      font-size: 0.85rem;
      line-height: 1.4;
      margin-top: 0.2rem;
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
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.25);
      transform: translateY(-1px);
    }

    /* Textarea */
    textarea {
      width: 100%;
      height: 155px;
      background: rgba(11, 19, 43, 0.6);
      border: 1px solid var(--card-border);
      border-radius: 1rem;
      padding: 1rem;
      color: var(--text-main);
      font-family: 'Inter', sans-serif;
      font-size: 0.95rem;
      resize: vertical;
      transition: all 0.3s ease;
      line-height: 1.5;
    }

    textarea:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 15px var(--primary-glow);
    }

    textarea:disabled {
      opacity: 0.55;
      cursor: not-allowed;
    }

    .action-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 0.6rem;
      margin-bottom: 1.25rem;
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .btn-clear {
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.85rem;
      text-decoration: underline;
      transition: color 0.2s;
    }

    .btn-clear:hover { color: var(--text-main); }

    .action-status {
      display: flex;
      gap: 0.75rem;
      align-items: center;
    }

    /* Submit Button */
    .btn-submit {
      width: 100%;
      background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
      color: #031525;
      border: none;
      padding: 0.95rem;
      border-radius: 1rem;
      font-family: 'Outfit', sans-serif;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.6rem;
      box-shadow: 0 10px 25px -5px rgba(56, 189, 248, 0.4);
      transition: all 0.25s ease;
    }

    .btn-submit:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 15px 30px -5px rgba(56, 189, 248, 0.55);
      background: linear-gradient(135deg, #0369a1 0%, #7dd3fc 100%);
    }

    .btn-submit:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }

    /* Right Result Card */
    .result-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 330px;
      text-align: center;
      color: var(--text-muted);
      gap: 1rem;
    }

    .result-placeholder svg {
      width: 48px;
      height: 48px;
      opacity: 0.35;
      stroke: var(--text-muted);
    }

    .result-content { display: none; }

    /* Hero Winner Category */
    .category-hero {
      border-radius: 1.25rem;
      padding: 1.25rem 1.4rem;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border: 1px solid transparent;
      animation: slideIn 0.35s ease;
    }

    @keyframes slideIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .cat-info {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .cat-icon {
      font-size: 2.2rem;
      line-height: 1;
    }

    .cat-name {
      font-family: 'Outfit', sans-serif;
      font-size: 1.45rem;
      font-weight: 800;
      letter-spacing: -0.01em;
    }

    .cat-subtitle {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .conf-badge { text-align: right; }

    .conf-score {
      font-family: 'Outfit', sans-serif;
      font-size: 1.6rem;
      font-weight: 800;
    }

    .conf-label {
      font-size: 0.78rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Probability Bars */
    .prob-section-title {
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 0.8rem;
    }

    .prob-item {
      margin-bottom: 0.9rem;
    }

    .prob-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.88rem;
      margin-bottom: 0.35rem;
    }

    .bar-bg {
      height: 7px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 9999px;
      overflow: hidden;
    }

    .bar-fill {
      height: 100%;
      border-radius: 9999px;
      transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* User Feedback & Copy */
    .user-tools {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1.5rem;
      padding-top: 1.25rem;
      border-top: 1px solid var(--card-border);
      flex-wrap: wrap;
      gap: 0.75rem;
    }

    .feedback-buttons {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .btn-feedback {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--card-border);
      padding: 0.35rem 0.65rem;
      border-radius: 0.5rem;
      cursor: pointer;
      transition: all 0.2s;
      font-size: 1rem;
    }

    .btn-feedback:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: scale(1.1);
    }

    .btn-copy {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 0.45rem 0.85rem;
      border-radius: 0.5rem;
      font-size: 0.85rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s;
    }

    .btn-copy:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
    }

    /* Themes for Categories */
    .theme-world { background: rgba(56, 189, 248, 0.12); border-color: rgba(56, 189, 248, 0.35); }
    .theme-world .conf-score, .theme-world .cat-name { color: var(--primary); }
    .theme-world .bar-fill { background: linear-gradient(90deg, #38bdf8, #0284c7); }

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
      z-index: 1000;
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
      <div class="header-badges">
        <div class="badge-status">
          <div class="dot-pulse"></div>
          <span>Sistema de Inteligencia Artificial Activo</span>
        </div>
        <div class="badge-token-header">
          <span>🎫 Tokens:</span>
          <span id="headerTokenBadge">20 / 20</span>
        </div>
      </div>
      <h1>Clasificador Inteligente de Noticias</h1>
      <p class="subtitle">Escribe o pega cualquier noticia en español para clasificar su categoría al instante.</p>
    </header>

    <!-- Main Grid -->
    <div class="grid">
      
      <!-- Input Card -->
      <div class="glass-card">
        <div class="card-title">
          <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
          Noticia a Analizar
        </div>

        <!-- Token Quota Widget (Sin reloj permanente) -->
        <div class="token-widget" id="tokenWidget">
          <div class="token-header">
            <div class="token-info">
              <span>🎫</span>
              <span>Tokens Disponibles:</span>
              <span class="token-badge" id="tokenCount">20 / 20</span>
            </div>
            <div class="token-status-text" id="tokenStatusText">
              <span>● Activo</span>
            </div>
          </div>
          <div class="token-progress-bg">
            <div class="token-progress-fill" id="tokenFill" style="width: 100%;"></div>
          </div>
          <div class="token-alert-banner" id="tokenAlert">
            ⚠️ Has agotado tus 20 tokens disponibles. Se reactivarán a las <strong id="tokenReactivationTime">--:-- hrs</strong>.
          </div>
        </div>

        <div class="presets-label">Prueba con ejemplos rápidos:</div>
        <div class="presets-grid">
          <button class="btn-preset" onclick="setPreset('world')">🌐 <span>Mundo</span></button>
          <button class="btn-preset" onclick="setPreset('sports')">⚽ <span>Deportes</span></button>
          <button class="btn-preset" onclick="setPreset('business')">📈 <span>Economía</span></button>
          <button class="btn-preset" onclick="setPreset('scitech')">💻 <span>Tecnología</span></button>
        </div>

        <textarea id="newsText" placeholder="Pega o escribe aquí el texto o titular de la noticia en español..."></textarea>
        
        <div class="action-bar">
          <button class="btn-clear" onclick="clearText()">Borrar texto</button>
          <div class="action-status">
            <span>🎫 <strong id="actionTokenCount">20/20</strong> tokens</span>
            <span>•</span>
            <div class="char-counter"><span id="charCount">0</span> caracteres</div>
          </div>
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
    // ══════════════════════════════════════════════════════════════════════════
    // ⚙️ CONFIGURACIÓN DE TOKENS EN LA INTERFAZ WEB
    // Modifica estas dos variables para ajustar la cuota y minutos en el frontend:
    // ══════════════════════════════════════════════════════════════════════════
    const TOKEN_MAX = 20;       // <- Línea 707: Cantidad máxima de consultas permitidas
    const TOKEN_RESET_MIN = 5;  // <- Línea 708: Minutos tras agotarse para reactivar
    // ══════════════════════════════════════════════════════════════════════════

    let remainingTokens = TOKEN_MAX;
    let pollInterval = null;

    function updateTokenUI(remaining, maxTokens, isExhausted, secondsLeft) {
      remainingTokens = remaining;

      const countEl = document.getElementById("tokenCount");
      const headerBadgeEl = document.getElementById("headerTokenBadge");
      const actionBadgeEl = document.getElementById("actionTokenCount");
      const statusTextEl = document.getElementById("tokenStatusText");
      const fillEl = document.getElementById("tokenFill");
      const widgetEl = document.getElementById("tokenWidget");
      const alertEl = document.getElementById("tokenAlert");
      const btn = document.getElementById("btnSubmit");
      const btnText = document.getElementById("btnText");

      if (countEl) countEl.textContent = `${remaining} / ${maxTokens}`;
      if (headerBadgeEl) headerBadgeEl.textContent = `${remaining} / ${maxTokens}`;
      if (actionBadgeEl) actionBadgeEl.textContent = `${remaining}/${maxTokens}`;

      const pct = Math.max(0, Math.min(100, (remaining / maxTokens) * 100));
      if (fillEl) fillEl.style.width = pct + "%";

      if (widgetEl) {
        widgetEl.classList.remove("low", "empty");
        if (remaining === 0) {
          widgetEl.classList.add("empty");
        } else if (remaining <= 5) {
          widgetEl.classList.add("low");
        }
      }

      if (remaining <= 0) {
        // Calcular la hora exacta de reactivación según el reloj local (ej: 14:35 hrs)
        const waitSecs = (typeof secondsLeft === "number" && secondsLeft > 0) ? secondsLeft : (TOKEN_RESET_MIN * 60);
        const targetDate = new Date(Date.now() + waitSecs * 1000);
        const hours = String(targetDate.getHours()).padStart(2, "0");
        const minutes = String(targetDate.getMinutes()).padStart(2, "0");
        const timeStr = `${hours}:${minutes}`;

        if (statusTextEl) statusTextEl.innerHTML = `<span style="color:#ef4444">● Reactiva a las ${timeStr} hrs</span>`;
        if (alertEl) {
          alertEl.innerHTML = `⚠️ Has agotado tus ${maxTokens} tokens disponibles. Se reactivarán a las <strong>${timeStr} hrs</strong>.`;
          alertEl.style.display = "block";
        }
        if (btn) btn.disabled = true;
        if (btnText) btnText.textContent = `⏳ Tokens agotados — Reactiva a las ${timeStr} hrs`;
        txtArea.disabled = true;
      } else {
        if (statusTextEl) statusTextEl.innerHTML = `<span style="color:#4ade80">● Activo</span>`;
        if (alertEl) alertEl.style.display = "none";
        if (btn && !btn.classList.contains("loading")) {
          btn.disabled = false;
          if (btnText) btnText.textContent = "✨ Clasificar Noticia";
        }
        txtArea.disabled = false;
      }
    }

    async function syncTokenStatus() {
      try {
        const res = await fetch("/token/status");
        if (res.ok) {
          const data = await res.json();
          updateTokenUI(data.remaining, data.max_questions, data.is_exhausted, data.reset_seconds);
          
          // Si los tokens se reactivaron después de haber estado en 0
          if (data.remaining > 0 && remainingTokens === 0) {
            showToast("🎉 ¡Tus 20 tokens han sido reactivados!");
          }
        }
      } catch (e) {
        console.warn("No se pudo sincronizar token:", e);
      }
    }

    // Polling ligero cada 10 segundos en caso de que esté agotado, para reactivar automáticamente tras 5 min
    function startTokenWatcher() {
      if (pollInterval) clearInterval(pollInterval);
      pollInterval = setInterval(() => {
        if (remainingTokens <= 0) {
          syncTokenStatus();
        }
      }, 8000);
    }

    const PRESETS = {
      world: "Líderes de diversos países se reúnen en la Cumbre Internacional de Ginebra para firmar un tratado histórico de paz y diplomacia.",
      sports: "El Real Madrid asegura la victoria en la final de la Champions League tras anotar dos goles decisivos en el tiempo reglamentario.",
      business: "Las acciones de la bolsa de valores alcanzan máximos históricos luego de que el Banco Central anunciara una baja en las tasas de interés.",
      scitech: "OpenAI y Microsoft presentan un nuevo avance revolucionario en Inteligencia Artificial capaz de procesar texto y código al instante."
    };

    const ICON_MAP = {
      "Mundo": "🌐", "Global": "🌐", "World": "🌐",
      "Deportes": "⚽", "Sports": "⚽",
      "Economía": "📈", "Negocios": "📈", "Business": "📈",
      "Tecnología": "💻", "Ciencia": "💻", "Tech": "💻"
    };

    const THEME_MAP = {
      "Mundo": "theme-world", "Global": "theme-world", "World": "theme-world",
      "Deportes": "theme-sports", "Sports": "theme-sports",
      "Economía": "theme-business", "Negocios": "theme-business", "Business": "theme-business",
      "Tecnología": "theme-scitech", "Ciencia": "theme-scitech", "Tech": "theme-scitech"
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
      setTimeout(() => { toast.style.display = "none"; }, 3500);
    }

    async function classifyNews() {
      if (remainingTokens <= 0) {
        showToast("⏳ Has alcanzado el límite de preguntas. Se reactivarán a la hora indicada en el recuadro rojo.");
        return;
      }

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

        if (response.status === 429) {
          const errData = await response.json();
          showToast("⛔ " + (errData.detail || "Has alcanzado el límite de tokens."));
          syncTokenStatus();
          return;
        }

        if (!response.ok) throw new Error("Error en la conexión con el servidor.");

        const data = await response.json();
        if (data.tokens_remaining !== undefined) {
          updateTokenUI(data.tokens_remaining, TOKEN_MAX, data.tokens_remaining <= 0, data.reset_seconds);
        }
        displayResults(data);

      } catch (err) {
        showToast("❌ " + err.message);
      } finally {
        spinner.style.display = "none";
        if (remainingTokens > 0) {
          btnText.textContent = "✨ Clasificar Noticia";
          btn.disabled = false;
        }
      }
    }

    // Inicializar sincronización de token y observador
    window.addEventListener("DOMContentLoaded", () => {
      syncTokenStatus();
      startTokenWatcher();
    });

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
