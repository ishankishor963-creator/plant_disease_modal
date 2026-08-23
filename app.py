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

st.set_page_config(page_title="Smart Farming Assistant", page_icon="🌱", layout="centered")

st.title("🌱 Smart Farming Assistant")
st.write("Upload a photo of a crop leaf (tomato, potato, or pepper) to detect disease and get treatment advice.")


@st.cache_resource
def load_model():
    return tf.keras.models.load_model("plant_model_v3.keras")


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

    st.subheader("Result")
    # Make the class name a bit more readable
    display_name = predicted_class.replace("___", " - ").replace("__", " ").replace("_", " ")

    if confidence < 70:
        st.error("This doesn't look like any of the 14 supported crops (apple, blueberry, cherry, corn, grape, orange, peach, pepper, potato, raspberry, soybean, squash, strawberry, tomato). Try a photo of one of these crops for a reliable result.")
    else:
        st.write(f"**Prediction:** {display_name}")
        st.write(f"**Confidence:** {confidence:.1f}%")

        if confidence < 85:
            st.warning("Confidence is moderate — consider taking a clearer, well-lit photo of a single leaf for a more reliable result.")

        info = RECOMMENDATIONS.get(predicted_class)
        if info:
            st.markdown("---")
            st.subheader("What this means")
            st.write(info["description"])
            st.subheader("Recommended action")
            st.write(info["treatment"])

st.markdown("---")
st.subheader("🌦️ Irrigation Tip")
city = st.text_input("Enter your city/location for a weather-based irrigation tip")

if city:
    api_key = st.secrets.get("OPENWEATHER_API_KEY", None)
    if not api_key:
        st.info("Weather feature not configured — add an OpenWeatherMap API key in app secrets to enable this.")
    else:
        weather_data = get_weather(city, api_key)
        if weather_data:
            temp = weather_data["main"]["temp"]
            condition = weather_data["weather"][0]["description"].title()
            st.write(f"**{city}:** {condition}, {temp}°C")
            st.write(get_irrigation_tip(weather_data))
        else:
            st.warning("Couldn't fetch weather for that location — check the spelling or try a nearby larger city/town name.")
