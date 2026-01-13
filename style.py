coldplay_css = """
/* --- GLOBAL THEME: Deep Space & Neon Aurora --- */
body, .gradio-container {
    background: linear-gradient(135deg, #0b0f19 0%, #101827 100%) !important;
    color: #e2e8f0 !important;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* --- TYPOGRAPHY: Elegant & Spaced --- */
/* Using a system serif for headers to evoke a premium editorial feel */
h1, h2, h3 {
    font-family: 'Georgia', 'Times New Roman', serif !important;
    letter-spacing: 0.05em !important;
    color: #ffffff !important;
    font-weight: 300 !important;
}

h1 {
    font-size: 2.5rem !important;
    text-align: center;
    background: -webkit-linear-gradient(0deg, #00f2ea, #ff0050);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.5rem !important;
}

/* --- BUTTONS: High Contrast & Neon Glow --- */
button.primary-btn, .primary {
    background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    border-radius: 4px !important;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 198, 255, 0.4);
}

button.primary-btn:hover, .primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 198, 255, 0.6);
}

/* --- CONTAINERS & PANELS --- */
/* Glassmorphism effect for blocks */
.block, .panel, .box {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    backdrop-filter: blur(10px);
}

/* --- TABS --- */
.tab-nav button {
    font-family: 'Georgia', serif !important;
    color: #94a3b8 !important;
    border: none !important;
}

.tab-nav button.selected {
    color: #00f2ea !important; /* Cyan accent */
    border-bottom: 2px solid #00f2ea !important;
    background: transparent !important;
    font-weight: bold;
}

/* --- TEXTBOXES & INPUTS --- */
input, textarea, .textbox {
    background-color: #1a202c !important;
    border: 1px solid #2d3748 !important;
    color: #ffffff !important;
    border-radius: 4px !important;
}

input:focus, textarea:focus {
    border-color: #00f2ea !important;
    box-shadow: 0 0 0 2px rgba(0, 242, 234, 0.2) !important;
}

/* --- PLOTLY CHART BACKGROUND FIX --- */
/* Ensures charts blend into the dark theme */
.js-plotly-plot .plotly .main-svg {
    background: rgba(0,0,0,0) !important;
}
"""
