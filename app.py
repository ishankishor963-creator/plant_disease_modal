import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import requests

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
# Design system: fonts, colors, and component styling
# ---------------------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">

<style>
:root {
    --color-bg: #FAF9F5;
    --color-surface: #FFFFFF;
    --color-primary: #2D5A3D;
    --color-primary-dark: #1B3B27;
    --color-accent: #C9A227;
    --color-soil: #6B4423;
    --color-text: #1F2421;
    --color-text-muted: #5B645D;
    --color-danger: #B3261E;
    --color-border: #E4E0D4;
}

.stApp { background-color: var(--color-bg); }
body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--color-text); }
h1, h2, h3 { font-family: 'Fraunces', serif; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
    border-radius: 16px;
    padding: 2.2rem 2rem;
    margin-bottom: 1.8rem;
    color: #F5F3EA;
    position: relative;
}
.hero-team {
    position: absolute;
    top: 1.4rem;
    right: 1.6rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #D9E4DB;
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
}
.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--color-accent);
    margin-bottom: 0.5rem;
}
.hero h1 {
    font-size: 2.1rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: #FFFFFF;
}
.hero p {
    font-size: 0.98rem;
    color: #D9E4DB;
    margin: 0;
    max-width: 34rem;
}

/* Cards */
.card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.4rem;
}
.eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--color-soil) !important;
    margin-bottom: 0.4rem;
}
.result-title {
    font-family: 'Fraunces', serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--color-primary-dark) !important;
    margin: 0 0 1rem 0;
}

/* Confidence gauge */
.gauge-wrap { margin-bottom: 1.2rem; }
.gauge-label {
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: var(--color-text-muted);
    margin-bottom: 0.35rem;
}
.gauge-value { font-weight: 600; color: var(--color-text); }
.gauge-track {
    width: 100%;
    height: 10px;
    background: #EFEBDD;
    border-radius: 6px;
    overflow: hidden;
}
.gauge-fill {
    height: 100%;
    border-radius: 6px;
}

/* Recommendation grid */
.rec-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.2rem;
    margin-top: 0.4rem;
}
@media (max-width: 640px) {
    .rec-grid { grid-template-columns: 1fr; }
}
.rec-box {
    padding: 1rem 1.1rem;
    border-radius: 10px;
    background: #F5F3EA;
    border-left: 3px solid var(--color-primary);
}
.rec-box.treatment { border-left-color: var(--color-accent); }
.rec-box h4 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-muted) !important;
    margin: 0 0 0.5rem 0;
    font-weight: 600;
}
.rec-box p {
    margin: 0;
    font-size: 0.93rem;
    line-height: 1.5;
    color: var(--color-text) !important;
}

/* Not-a-supported-crop banner */
.unrecognized {
    border-left: 3px solid var(--color-danger);
    background: #FBEDEB;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.92rem;
}

[data-testid="stFileUploader"] section {
    border: 2px dashed var(--color-soil);
    border-radius: 12px;
    background: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-team">Team Cyberpunk</div>
    <div class="hero-eyebrow">Field Diagnostics</div>
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
        return "#2D5A3D"  # confident — primary green
    elif pct >= 70:
        return "#C9A227"  # moderate — accent gold
    else:
        return "#B3261E"  # low — danger red


_, popover_col = st.columns([3, 1])
with popover_col:
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
                        <p style="margin:0 0 0.4rem 0; font-weight:600;">{city} — {condition}, {temp}°C</p>
                        <p style="margin:0; font-size:0.92rem;">{tip}</p>
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

    with st.spinner("Analyzing..."):
        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions[0])
        predicted_class = CLASS_NAMES[predicted_index]
        confidence = 100 * np.max(predictions[0])

    display_name = predicted_class.replace("___", " - ").replace("__", " ").replace("_", " ")

    if confidence < 70:
        st.markdown(f"""
        <div class="card">
            <div class="eyebrow">Diagnosis</div>
            <div class="unrecognized">
                This doesn't look like any of the 14 supported crops ({SUPPORTED_CROPS}).
                Try a photo of one of these crops for a reliable result.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        color = gauge_color(confidence)
        confidence_note = "" if confidence >= 85 else '<p style="margin-top:0.8rem; font-size:0.86rem; color:var(--color-text-muted);">Confidence is moderate — a clearer, well-lit photo of a single leaf may improve accuracy.</p>'

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
                    <div class="gauge-fill" style="width:{confidence:.1f}%; background:{color};"></div>
                </div>
            </div>
            {confidence_note}
        </div>
        """, unsafe_allow_html=True)

        info = RECOMMENDATIONS.get(predicted_class)
        if info:
            st.markdown(f"""
            <div class="card">
                <div class="eyebrow">Treatment Plan</div>
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
