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
# Design system — dark crop-intelligence HUD aesthetic
# ---------------------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">

<style>
:root {
    --bg: #0A0E0C;
    --surface: #121815;
    --surface-2: #1A211D;
    --border: rgba(255,255,255,0.09);
    --text: #E7F2EC;
    --text-muted: #93A99C;
    --accent: #A6FF3C;
    --accent-2: #34E4C0;
    --warn: #FFC857;
    --danger: #FF6B5C;
    --glow: rgba(166,255,60,0.28);
}

#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background-color: var(--bg);
    background-image:
        linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 34px 34px;
}
body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--text); }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

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

/* Hero */
.hero {
    background: linear-gradient(160deg, #101A14 0%, #0D1310 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2.4rem 2.2rem;
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
    top: 1.5rem; right: 1.7rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-2);
    border: 1px solid rgba(52,228,192,0.35);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
}
.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.6rem;
}
.hero h1 {
    font-size: 2.3rem;
    font-weight: 700;
    margin: 0 0 0.6rem 0;
    color: #FFFFFF;
    text-shadow: 0 0 22px rgba(166,255,60,0.25);
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
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.7rem 1.9rem;
    margin-bottom: 1.3rem;
    position: relative;
    animation: fadeInUp 0.45s ease both;
}
.card::before {
    content: "";
    position: absolute;
    top: 0; left: 1.6rem; right: 1.6rem;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0.6;
}
.eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent-2) !important;
    margin-bottom: 0.6rem;
    font-weight: 600;
}
.result-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #FFFFFF !important;
    margin: 0 0 1.1rem 0;
}

/* Confidence gauge */
.gauge-wrap { margin-bottom: 0.3rem; }
.gauge-label {
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted) !important;
    margin-bottom: 0.5rem;
    letter-spacing: 0.04em;
}
.gauge-value { font-weight: 600; color: var(--text) !important; }
.gauge-track {
    width: 100%;
    height: 10px;
    background: #1E2620;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border);
}
.gauge-fill {
    height: 100%;
    border-radius: 6px;
    animation: growFill 1s cubic-bezier(0.22, 1, 0.36, 1) both;
}

/* Recommendation grid */
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
    background: var(--surface-2);
    border-left: 3px solid var(--accent);
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
}
.rec-box.treatment { border-left-color: var(--accent-2); }
.rec-box h4 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin: 0 0 0.6rem 0;
    font-weight: 600;
}
.rec-box p {
    margin: 0;
    font-size: 0.93rem;
    line-height: 1.55;
    color: var(--text) !important;
}

/* Unrecognized-crop alert */
.unrecognized {
    border: 1px solid rgba(255,107,92,0.35);
    background: rgba(255,107,92,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    font-size: 0.92rem;
    color: var(--text) !important;
}
.unrecognized-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--danger) !important;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

/* Scan sequence */
.scan-card {
    background: var(--surface);
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
    background: #1E2620;
    border-radius: 2px;
    overflow: hidden;
    margin: 0.9rem 0 1.1rem 0;
}
.scan-bar {
    position: absolute;
    top: 0; height: 100%; width: 30%;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    animation: scanSweep 1.3s linear infinite;
}
.scan-line {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-muted);
    margin: 0.35rem 0;
    animation: pulseGlow 1.6s ease-in-out infinite;
}
.scan-line span { color: var(--accent-2); }

/* File uploader */
[data-testid="stFileUploader"] section {
    border: 2px dashed rgba(166,255,60,0.4);
    border-radius: 14px;
    background: var(--surface);
}
[data-testid="stFileUploader"] label p { color: var(--text-muted) !important; }

/* Popover trigger button */
[data-testid="stPopover"] button, .stPopover button {
    background: var(--surface) !important;
    border: 1px solid rgba(52,228,192,0.4) !important;
    color: var(--accent-2) !important;
    border-radius: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em !important;
}

/* Footer */
.sys-footer {
    font-family: 'IBM Plex Mono', monospace;
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
    <div class="hero-eyebrow">// Field Diagnostics System</div>
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


def get_soil_moisture():
    """Fetch latest soil moisture reading from ThingSpeak."""
    channel_id = "3467712"
    read_api_key = "GV82FOVOEX7A2MQU"
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {"api_key": read_api_key, "results": 1}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("feeds"):
                return data["feeds"][0]
        return None
    except requests.exceptions.RequestException:
        return None


def gauge_color(pct):
    if pct >= 85:
        return "#A6FF3C"  # confident — accent lime
    elif pct >= 70:
        return "#FFC857"  # moderate — amber
    else:
        return "#FF6B5C"  # low — danger red


_, soil_col, weather_col = st.columns([2, 1, 1])

with soil_col:
    with st.popover("🌱 Soil Moisture", use_container_width=True):
        st.markdown('<div class="eyebrow">Live Sensor Feed</div>', unsafe_allow_html=True)
        soil_data = get_soil_moisture()
        if soil_data and soil_data.get("field1") is not None:
            moisture = float(soil_data["field1"])
            timestamp = soil_data["created_at"]
            color = gauge_color(moisture)

            st.markdown(f"""
            <div class="gauge-wrap" style="margin-top:0.6rem;">
                <div class="gauge-label">
                    <span>Moisture Level</span>
                    <span class="gauge-value">{moisture:.0f}%</span>
                </div>
                <div class="gauge-track">
                    <div class="gauge-fill" style="width:{moisture:.0f}%; background:{color}; box-shadow: 0 0 12px {color}77;"></div>
                </div>
            </div>
            <p style="margin-top:0.9rem; font-size:0.8rem; color:var(--text-muted); font-family:'IBM Plex Mono', monospace;">Last updated: {timestamp}</p>
            """, unsafe_allow_html=True)
        else:
            st.warning("Couldn't fetch soil moisture data — check the sensor and ThingSpeak connection.")

with weather_col:
    with st.popover("🌦️ Irrigation Tip", use_container_width=True):
        st.markdown('<div class="eyebrow">Field Conditions</div>', unsafe_allow_html=True)
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
                    <div style="margin-top:0.6rem;">
                        <p style="margin:0 0 0.4rem 0; font-weight:600; color:var(--text);">{city} — {condition}, {temp}°C</p>
                        <p style="margin:0; font-size:0.92rem; color:var(--text);">{tip}</p>
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
        <div class="eyebrow">Analyzing Sample</div>
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
            <div class="eyebrow">Diagnosis</div>
            <div class="unrecognized">
                <div class="unrecognized-label">⚠ Crop Not Recognized</div>
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
            <div class="eyebrow">Diagnosis</div>
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
                <div class="eyebrow">Treatment Protocol</div>
                <div class="rec-grid">
                    <div class="rec-box">
                        <h4>What This Means</h4>
                        <p>{info["description"]}</p>
                    </div>
                    <div class="rec-box treatment">
                        <h4>Recommended Action</h4>
                        <p>{info["treatment"]}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div class="sys-footer">Agro Edge // Crop Intelligence System // Team Cyberpunk</div>', unsafe_allow_html=True)
