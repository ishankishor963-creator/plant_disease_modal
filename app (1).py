
App · PY
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import requests
import time
 
from recommendations import RECOMMENDATIONS
 
# Class names must be in the same order the model was trained on
CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]
 
SUPPORTED_CROPS = "apple, blueberry, cherry, corn, grape, orange, peach, pepper, potato, raspberry, soybean, squash, strawberry, tomato"
 
st.set_page_config(page_title="Agro Edge", page_icon="🌱", layout="centered")
 
# ---------------------------------------------------------------------------
# Design system — AgriPulse-inspired glass-panel aesthetic, adapted for
# Streamlit. Same color tokens, fonts and card language as the AgriPulse
# reference UI, applied on top of the existing Agro Edge functionality.
# ---------------------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
 
<style>
:root {
    /* AgriPulse color tokens */
    --bg: #111410;
    --surface: #1d201c;
    --surface-2: #191c18;
    --surface-high: #282b26;
    --surface-highest: #333631;
    --border: rgba(224,242,241,0.12);
    --border-strong: rgba(224,242,241,0.22);
    --text: #e2e3dc;
    --text-muted: #c2c9bb;
    --sky-tint: #E0F2F1;
    --sapling-green: #7DBE6F;
    --primary: #a1d494;
    --primary-container: #2d5a27;
    --secondary: #e9c349;
    --harvest-gold: #F2C94C;
    --soil-brown: #4B3621;
    --tertiary: #ffb0cc;
    --error: #ffb4ab;
    --error-container: #93000a;
    --glow: rgba(224,242,241,0.18);
}
 
#MainMenu, footer, header { visibility: hidden; }
 
.stApp {
    background-color: var(--bg);
    background-image:
        radial-gradient(circle at 15% 0%, rgba(224,242,241,0.06) 0%, transparent 45%),
        radial-gradient(circle at 100% 30%, rgba(161,212,148,0.05) 0%, transparent 40%);
}
body, [class*="css"] { font-family: 'Hanken Grotesk', sans-serif; color: var(--text); }
h1, h2, h3 { font-family: 'Hanken Grotesk', sans-serif; }
 
.material-symbols-outlined {
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    vertical-align: middle;
}
 
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.55; }
}
@keyframes scanSweep {
    0% { left: -30%; }
    100% { left: 110%; }
}
@keyframes growFill {
    from { width: 0%; }
}
 
/* Glass panel base, matching AgriPulse's .glass-card */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    border: 1px solid var(--border);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
}
 
/* Hero */
.hero {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(14px) saturate(150%);
    -webkit-backdrop-filter: blur(14px) saturate(150%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2.2rem 2.2rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s ease both;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60%; right: -20%;
    width: 60%; height: 220%;
    background: radial-gradient(circle, var(--glow) 0%, transparent 70%);
    pointer-events: none;
}
.hero-team {
    position: absolute;
    top: 1.4rem; right: 1.6rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--sky-tint);
    border: 1px solid var(--border-strong);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
}
.hero-eyebrow {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sapling-green);
    margin-bottom: 0.6rem;
}
.hero h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 0.6rem 0;
    color: var(--sapling-green);
}
.hero p {
    font-size: 0.98rem;
    color: var(--text-muted);
    margin: 0;
    max-width: 32rem;
    line-height: 1.55;
}
 
/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.7rem 1.9rem;
    margin-bottom: 1.3rem;
    position: relative;
    animation: fadeInUp 0.45s ease both;
}
.eyebrow {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin-bottom: 0.6rem;
    font-weight: 500;
}
.result-title {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--sapling-green) !important;
    margin: 0 0 1.1rem 0;
}
 
/* Confidence gauge */
.gauge-wrap { margin-bottom: 0.3rem; }
.gauge-label {
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted) !important;
    margin-bottom: 0.5rem;
    letter-spacing: 0.03em;
}
.gauge-value { font-weight: 600; color: var(--text) !important; }
.gauge-track {
    width: 100%;
    height: 10px;
    background: var(--surface-highest);
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border);
}
.gauge-fill {
    height: 100%;
    border-radius: 6px;
    animation: growFill 1s cubic-bezier(0.22, 1, 0.36, 1) both;
}
 
/* Recommendation grid — bento style */
.rec-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.1rem;
    margin-top: 0.3rem;
}
@media (max-width: 640px) {
    .rec-grid { grid-template-columns: 1fr; }
}
.rec-box {
    padding: 1.1rem 1.2rem;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-left: 3px solid var(--sapling-green);
}
.rec-box.treatment { border-left-color: var(--secondary); }
.rec-box h4 {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin: 0 0 0.6rem 0;
    font-weight: 500;
}
.rec-box p {
    margin: 0;
    font-size: 0.93rem;
    line-height: 1.55;
    color: var(--text) !important;
}
 
/* Unrecognized-crop alert */
.unrecognized {
    border: 1px solid rgba(255,180,171,0.35);
    background: rgba(255,180,171,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    font-size: 0.92rem;
    color: var(--text) !important;
}
.unrecognized-label {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--error) !important;
    margin-bottom: 0.5rem;
    font-weight: 500;
}
 
/* Scan sequence */
.scan-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.3rem;
    position: relative;
    overflow: hidden;
}
.scan-track {
    position: relative;
    width: 100%;
    height: 3px;
    background: var(--surface-highest);
    border-radius: 2px;
    overflow: hidden;
    margin: 0.9rem 0 1.1rem 0;
}
.scan-bar {
    position: absolute;
    top: 0; height: 100%; width: 30%;
    background: linear-gradient(90deg, transparent, var(--sapling-green), transparent);
    animation: scanSweep 1.3s linear infinite;
}
.scan-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-muted);
    margin: 0.35rem 0;
    animation: pulseGlow 1.6s ease-in-out infinite;
}
.scan-line span { color: var(--sky-tint); }
 
/* Weather / irrigation panel (AgriPulse hero-weather-card styling) */
.weather-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px) saturate(150%);
    -webkit-backdrop-filter: blur(12px) saturate(150%);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-top: 0.6rem;
}
.weather-card .place-line {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-weight: 600;
    color: var(--sky-tint);
    margin: 0 0 0.4rem 0;
    font-family: 'Hanken Grotesk', sans-serif;
}
.weather-card .tip-line {
    margin: 0;
    font-size: 0.92rem;
    color: var(--text);
    line-height: 1.5;
}
 
/* File uploader */
[data-testid="stFileUploader"] section {
    border: 2px dashed rgba(224,242,241,0.35);
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
}
[data-testid="stFileUploader"] label p { color: var(--text-muted) !important; }
 
/* Popover trigger button */
[data-testid="stPopover"] button, .stPopover button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border-strong) !important;
    color: var(--sky-tint) !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
}
 
/* Footer */
.sys-footer {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    text-align: center;
    padding: 1.4rem 0 0.6rem 0;
    border-top: 1px solid var(--border);
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)
 
# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-team">Team Cyberpunk</div>
    <div class="hero-eyebrow">
        <span class="material-symbols-outlined" style="font-size:16px;">energy_savings_leaf</span>
        Field Diagnostics System
    </div>
    <h1>🌱 Agro Edge</h1>
    <p>Upload a photo of a crop leaf to detect disease and get treatment advice — plus a weather-based irrigation tip for your location.</p>
</div>
""", unsafe_allow_html=True)
 
 
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("plant_model_v4.keras")
 
 
model = load_model()
 
 
def get_weather(city_name, api_key):
    """Fetch current weather for a city using OpenWeatherMap. Returns dict or None on failure."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None
 
 
def get_irrigation_tip(weather_data):
    """Simple rule-based irrigation advice based on current conditions."""
    condition = weather_data["weather"][0]["main"].lower()
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
 
    if "rain" in condition or "drizzle" in condition or "thunderstorm" in condition:
        return "🌧️ Rain detected — delay watering to avoid overwatering and root issues."
    elif temp > 32 and humidity < 40:
        return "☀️ Hot and dry conditions — consider watering soon, ideally early morning or evening to reduce evaporation."
    elif humidity > 80:
        return "💧 High humidity — go easy on watering, and monitor for fungal disease risk (many crop diseases spread faster in humid conditions)."
    else:
        return "🌤️ Conditions look moderate — water as per your crop's normal schedule."
 
 
def gauge_color(pct):
    if pct >= 85:
        return "#7DBE6F"  # confident — sapling green
    elif pct >= 70:
        return "#e9c349"  # moderate — amber
    else:
        return "#ffb4ab"  # low — error red
 
 
_, popover_col = st.columns([3, 1])
with popover_col:
    with st.popover("🌦️ Irrigation Tip", use_container_width=True):
        st.markdown(
            '<div class="eyebrow">'
            '<span class="material-symbols-outlined" style="font-size:14px;">location_on</span>'
            'Field Conditions</div>',
            unsafe_allow_html=True,
        )
        city = st.text_input("Place name", placeholder="Enter your city/location")
 
        if city:
            api_key = st.secrets.get("OPENWEATHER_API_KEY", None)
            if not api_key:
                st.info("Weather feature not configured — add an OpenWeatherMap API key in app secrets to enable this.")
            else:
                weather_data = get_weather(city, api_key)
                if weather_data:
                    temp = weather_data["main"]["temp"]
                    condition = weather_data["weather"][0]["description"].title()
                    tip = get_irrigation_tip(weather_data)
                    st.markdown(f"""
                    <div class="weather-card">
                        <p class="place-line">
                            <span class="material-symbols-outlined" style="font-size:18px;">location_on</span>
                            {city} — {condition}, {temp}°C
                        </p>
                        <p class="tip-line">{tip}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Couldn't fetch weather for that location — check the spelling or try a nearby larger city/town name.")
 
 
uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])
 
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image", use_container_width=True)
 
    # Preprocess exactly like training: resize to 224x224
    img_resized = image.resize((224, 224))
    img_array = np.array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)  # add batch dimension
 
    scan_placeholder = st.empty()
    scan_placeholder.markdown("""
    <div class="scan-card">
        <div class="eyebrow">
            <span class="material-symbols-outlined" style="font-size:14px;">biotech</span>
            Analyzing Sample
        </div>
        <div class="scan-track"><div class="scan-bar"></div></div>
        <div class="scan-line">&gt; <span>Extracting visual features...</span></div>
        <div class="scan-line">&gt; <span>Cross-referencing 38 crop-disease profiles...</span></div>
        <div class="scan-line">&gt; <span>Computing confidence score...</span></div>
    </div>
    """, unsafe_allow_html=True)
 
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = 100 * np.max(predictions[0])
 
    time.sleep(0.4)  # let the scan animation register before revealing the result
    scan_placeholder.empty()
 
    display_name = predicted_class.replace("___", " - ").replace("__", " ").replace("_", " ")
 
    if confidence < 70:
        st.markdown(f"""
        <div class="card">
            <div class="eyebrow">
                <span class="material-symbols-outlined" style="font-size:14px;">search</span>
                Diagnosis
            </div>
            <div class="unrecognized">
                <div class="unrecognized-label">
                    <span class="material-symbols-outlined" style="font-size:16px;">warning</span>
                    Crop Not Recognized
                </div>
                This doesn't look like any of the 14 supported crops ({SUPPORTED_CROPS}).
                Try a photo of one of these crops for a reliable result.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        color = gauge_color(confidence)
        confidence_note = "" if confidence >= 85 else '<p style="margin-top:0.9rem; font-size:0.86rem; color:var(--text-muted);">Confidence is moderate — a clearer, well-lit photo of a single leaf may improve accuracy.</p>'
 
        st.markdown(f"""
        <div class="card">
            <div class="eyebrow">
                <span class="material-symbols-outlined" style="font-size:14px;">search</span>
                Diagnosis
            </div>
            <div class="result-title">{display_name}</div>
            <div class="gauge-wrap">
                <div class="gauge-label">
                    <span>Confidence</span>
                    <span class="gauge-value">{confidence:.1f}%</span>
                </div>
                <div class="gauge-track">
                    <div class="gauge-fill" style="width:{confidence:.1f}%; background:{color}; box-shadow: 0 0 12px {color}77;"></div>
                </div>
            </div>
            {confidence_note}
        </div>
        """, unsafe_allow_html=True)
 
        info = RECOMMENDATIONS.get(predicted_class)
        if info:
            st.markdown(f"""
            <div class="card">
                <div class="eyebrow">
                    <span class="material-symbols-outlined" style="font-size:14px;">agriculture</span>
                    Treatment Protocol
                </div>
                <div class="rec-grid">
                    <div class="rec-box">
                        <h4>
                            <span class="material-symbols-outlined" style="font-size:14px;">info</span>
                            What This Means
                        </h4>
                        <p>{info["description"]}</p>
                    </div>
                    <div class="rec-box treatment">
                        <h4>
                            <span class="material-symbols-outlined" style="font-size:14px;">medication</span>
                            Recommended Action
                        </h4>
                        <p>{info["treatment"]}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <div class="eyebrow">
                    <span class="material-symbols-outlined" style="font-size:14px;">agriculture</span>
                    Treatment Protocol
                </div>
                <p style="color:var(--text-muted); font-size:0.92rem; margin:0;">
                    No treatment info available for this diagnosis yet.
                </p>
            </div>
            """, unsafe_allow_html=True)
 
st.markdown('<div class="sys-footer">Agro Edge // Crop Intelligence System // Team Cyberpunk</div>', unsafe_allow_html=True)
 
