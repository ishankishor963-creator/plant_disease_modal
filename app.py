import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

from recommendations import RECOMMENDATIONS

# Class names must be in the same order the model was trained on
CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy",
]

st.set_page_config(page_title="Smart Farming Assistant", page_icon="🌱", layout="centered")

st.title("🌱 Smart Farming Assistant")
st.write("Upload a photo of a crop leaf (tomato, potato, or pepper) to detect disease and get treatment advice.")


@st.cache_resource
def load_model():
    return tf.keras.models.load_model("plant_model.keras")


model = load_model()

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
    st.write(f"**Prediction:** {display_name}")
    st.write(f"**Confidence:** {confidence:.1f}%")

    if confidence < 50:
        st.warning("Confidence is low — consider taking a clearer, well-lit photo of a single leaf for a more reliable result.")

    info = RECOMMENDATIONS.get(predicted_class)
    if info:
        st.markdown("---")
        st.subheader("What this means")
        st.write(info["description"])
        st.subheader("Recommended action")
        st.write(info["treatment"])
