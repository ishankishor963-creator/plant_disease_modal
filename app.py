

import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import requests
import time
import random
from deep_translator import GoogleTranslator
from ddgs import DDGS
 
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
 
# ---------------------------------------------------------------------------
# Language support
# ---------------------------------------------------------------------------
LANGUAGES = {
    "English": "en",
    "हिंदी": "hi",
    "മലയാളം": "ml",
    "ಕನ್ನಡ": "kn",
    "தமிழ்": "ta",
}
 
UI_STRINGS = {
    "en": {
        "eyebrow_system": "// Field Diagnostics System",
        "hero_desc": "Upload a photo of a crop leaf to detect disease and get treatment advice — plus a weather-based irrigation tip for your location.",
        "location_heading": "📍 Your Location (for weather theme & irrigation tip)",
        "location_placeholder": "Enter your city/location",
        "enter_location_hint": "Enter your location above to see the weather-based irrigation tip and theme.",
        "soil_button": "🌱 Soil Moisture",
        "soil_eyebrow": "Live Sensor Feed",
        "moisture_label": "Moisture Level",
        "soil_error": "Couldn't fetch soil moisture data — check the sensor and ThingSpeak connection.",
        "weather_button": "🌦️ Irrigation Tip",
        "weather_eyebrow": "Field Conditions",
        "weather_not_configured": "Weather feature not configured — add an OpenWeatherMap API key in app secrets to enable this.",
        "weather_error": "Couldn't fetch weather for that location — check the spelling or try a nearby larger city/town name.",
        "upload_label": "Upload a leaf image",
        "uploaded_caption": "Uploaded image",
        "analyzing_eyebrow": "Analyzing Sample",
        "scan_line1": "Extracting visual features...",
        "scan_line2": "Cross-referencing 38 crop-disease profiles...",
        "scan_line3": "Computing confidence score...",
        "diagnosis_eyebrow": "Diagnosis",
        "not_recognized_label": "⚠ Crop Not Recognized",
        "not_recognized_msg": "This doesn't look like any of the 14 supported crops ({crops}). Try a photo of one of these crops for a reliable result.",
        "confidence_label": "Confidence",
        "confidence_note": "Confidence is moderate — a clearer, well-lit photo of a single leaf may improve accuracy.",
        "treatment_eyebrow": "Treatment Protocol",
        "what_means_header": "What This Means",
        "recommended_action_header": "Recommended Action",
        "web_search_button": "🌐 Search the Web for More Info",
        "web_searching": "Searching the web for more information...",
        "web_info_eyebrow": "More Info from the Web",
        "web_no_results": "No web results found — try again in a moment.",
        "footer": "Agro Edge // Crop Intelligence System // Team Cyberpunk",
        "last_updated": "Last updated:",
    },
    "hi": {
        "eyebrow_system": "// फील्ड डायग्नोस्टिक्स सिस्टम",
        "hero_desc": "रोग की पहचान करने और उपचार सलाह पाने के लिए फसल की पत्ती की फोटो अपलोड करें — साथ ही आपके स्थान के लिए मौसम आधारित सिंचाई सुझाव भी।",
        "location_heading": "📍 आपका स्थान (मौसम थीम और सिंचाई सुझाव के लिए)",
        "location_placeholder": "अपना शहर/स्थान दर्ज करें",
        "enter_location_hint": "मौसम आधारित सिंचाई सुझाव और थीम देखने के लिए ऊपर अपना स्थान दर्ज करें।",
        "soil_button": "🌱 मिट्टी की नमी",
        "soil_eyebrow": "लाइव सेंसर फीड",
        "moisture_label": "नमी स्तर",
        "soil_error": "मिट्टी की नमी का डेटा नहीं मिल सका — सेंसर और थिंगस्पीक कनेक्शन जांचें।",
        "weather_button": "🌦️ सिंचाई सुझाव",
        "weather_eyebrow": "क्षेत्र की स्थिति",
        "weather_not_configured": "मौसम सुविधा कॉन्फ़िगर नहीं है — इसे सक्षम करने के लिए ऐप सीक्रेट्स में OpenWeatherMap API कुंजी जोड़ें।",
        "weather_error": "उस स्थान का मौसम नहीं मिल सका — वर्तनी जांचें या किसी नज़दीकी बड़े शहर का नाम आज़माएं।",
        "upload_label": "पत्ती की फोटो अपलोड करें",
        "uploaded_caption": "अपलोड की गई फोटो",
        "analyzing_eyebrow": "नमूने का विश्लेषण हो रहा है",
        "scan_line1": "दृश्य विशेषताएं निकाली जा रही हैं...",
        "scan_line2": "38 फसल-रोग प्रोफाइल से तुलना हो रही है...",
        "scan_line3": "विश्वास स्कोर की गणना हो रही है...",
        "diagnosis_eyebrow": "निदान",
        "not_recognized_label": "⚠ फसल पहचानी नहीं गई",
        "not_recognized_msg": "यह समर्थित 14 फसलों ({crops}) में से किसी जैसी नहीं दिखती। विश्वसनीय परिणाम के लिए इनमें से किसी एक फसल की फोटो आज़माएं।",
        "confidence_label": "विश्वास स्तर",
        "confidence_note": "विश्वास स्तर मध्यम है — एक स्पष्ट, अच्छी रोशनी वाली एकल पत्ती की फोटो सटीकता बढ़ा सकती है।",
        "treatment_eyebrow": "उपचार प्रोटोकॉल",
        "what_means_header": "इसका क्या अर्थ है",
        "recommended_action_header": "अनुशंसित कार्रवाई",
        "web_search_button": "🌐 अधिक जानकारी के लिए वेब खोजें",
        "web_searching": "अधिक जानकारी के लिए वेब खोजी जा रही है...",
        "web_info_eyebrow": "वेब से अधिक जानकारी",
        "web_no_results": "कोई वेब परिणाम नहीं मिला — कुछ देर बाद पुनः प्रयास करें।",
        "footer": "एग्रो एज // क्रॉप इंटेलिजेंस सिस्टम // टीम साइबरपंक",
        "last_updated": "आखिरी बार अपडेट किया गया:",
    },
    "ml": {
        "eyebrow_system": "// ഫീൽഡ് ഡയഗ്നോസ്റ്റിക്സ് സിസ്റ്റം",
        "hero_desc": "രോഗം കണ്ടെത്താനും ചികിത്സാ നിർദ്ദേശം ലഭിക്കാനും വിളയുടെ ഇലയുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക — കൂടാതെ നിങ്ങളുടെ സ്ഥലത്തിനുള്ള കാലാവസ്ഥാധിഷ്ഠിത ജലസേചന നിർദ്ദേശവും.",
        "location_heading": "📍 നിങ്ങളുടെ സ്ഥലം (കാലാവസ്ഥാ തീം & ജലസേചന നിർദ്ദേശത്തിന്)",
        "location_placeholder": "നിങ്ങളുടെ നഗരം/സ്ഥലം നൽകുക",
        "enter_location_hint": "കാലാവസ്ഥാധിഷ്ഠിത ജലസേചന നിർദ്ദേശവും തീമും കാണാൻ മുകളിൽ നിങ്ങളുടെ സ്ഥലം നൽകുക.",
        "soil_button": "🌱 മണ്ണിലെ ഈർപ്പം",
        "soil_eyebrow": "ലൈവ് സെൻസർ ഫീഡ്",
        "moisture_label": "ഈർപ്പ നില",
        "soil_error": "മണ്ണിലെ ഈർപ്പ ഡാറ്റ ലഭിച്ചില്ല — സെൻസറും ThingSpeak കണക്ഷനും പരിശോധിക്കുക.",
        "weather_button": "🌦️ ജലസേചന നിർദ്ദേശം",
        "weather_eyebrow": "സ്ഥല സാഹചര്യങ്ങൾ",
        "weather_not_configured": "കാലാവസ്ഥാ സവിശേഷത കോൺഫിഗർ ചെയ്തിട്ടില്ല — ഇത് സജീവമാക്കാൻ ആപ്പ് സീക്രട്ടുകളിൽ OpenWeatherMap API കീ ചേർക്കുക.",
        "weather_error": "ആ സ്ഥലത്തെ കാലാവസ്ഥ ലഭിച്ചില്ല — അക്ഷരവിന്യാസം പരിശോധിക്കുക അല്ലെങ്കിൽ അടുത്തുള്ള വലിയ നഗരത്തിന്റെ പേര് ശ്രമിക്കുക.",
        "upload_label": "ഇലയുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക",
        "uploaded_caption": "അപ്‌ലോഡ് ചെയ്ത ഫോട്ടോ",
        "analyzing_eyebrow": "സാമ്പിൾ വിശകലനം ചെയ്യുന്നു",
        "scan_line1": "ദൃശ്യ സവിശേഷതകൾ എടുക്കുന്നു...",
        "scan_line2": "38 വിള-രോഗ പ്രൊഫൈലുകളുമായി താരതമ്യം ചെയ്യുന്നു...",
        "scan_line3": "വിശ്വാസ്യതാ സ്കോർ കണക്കാക്കുന്നു...",
        "diagnosis_eyebrow": "രോഗനിർണയം",
        "not_recognized_label": "⚠ വിള തിരിച്ചറിഞ്ഞില്ല",
        "not_recognized_msg": "ഇത് പിന്തുണയ്ക്കുന്ന 14 വിളകളിൽ ({crops}) ഏതെങ്കിലുമായി പൊരുത്തപ്പെടുന്നില്ല. വിശ്വസനീയമായ ഫലത്തിനായി ഈ വിളകളിൽ ഒന്നിന്റെ ഫോട്ടോ ശ്രമിക്കുക.",
        "confidence_label": "വിശ്വാസ്യത",
        "confidence_note": "വിശ്വാസ്യത മിതമായ നിലയിലാണ് — വ്യക്തവും നല്ല വെളിച്ചമുള്ളതുമായ ഒറ്റ ഇലയുടെ ഫോട്ടോ കൃത്യത മെച്ചപ്പെടുത്തിയേക്കാം.",
        "treatment_eyebrow": "ചികിത്സാ പ്രോട്ടോക്കോൾ",
        "what_means_header": "ഇതിന്റെ അർത്ഥം",
        "recommended_action_header": "ശുപാർശ ചെയ്യുന്ന നടപടി",
        "web_search_button": "🌐 കൂടുതൽ വിവരങ്ങൾക്കായി വെബ് തിരയുക",
        "web_searching": "കൂടുതൽ വിവരങ്ങൾക്കായി വെബ് തിരയുന്നു...",
        "web_info_eyebrow": "വെബിൽ നിന്നുള്ള കൂടുതൽ വിവരങ്ങൾ",
        "web_no_results": "വെബ് ഫലങ്ങളൊന്നും കണ്ടെത്തിയില്ല — അൽപ്പസമയം കഴിഞ്ഞ് വീണ്ടും ശ്രമിക്കുക.",
        "footer": "അഗ്രോ എഡ്ജ് // ക്രോപ്പ് ഇന്റലിജൻസ് സിസ്റ്റം // ടീം സൈബർപങ്ക്",
        "last_updated": "അവസാനം അപ്ഡേറ്റ് ചെയ്തത്:",
    },
    "kn": {
        "eyebrow_system": "// ಫೀಲ್ಡ್ ಡಯಾಗ್ನೋಸ್ಟಿಕ್ಸ್ ಸಿಸ್ಟಮ್",
        "hero_desc": "ರೋಗ ಪತ್ತೆ ಮಾಡಲು ಮತ್ತು ಚಿಕಿತ್ಸಾ ಸಲಹೆ ಪಡೆಯಲು ಬೆಳೆಯ ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ — ಜೊತೆಗೆ ನಿಮ್ಮ ಸ್ಥಳಕ್ಕೆ ಹವಾಮಾನ ಆಧಾರಿತ ನೀರಾವರಿ ಸಲಹೆ.",
        "location_heading": "📍 ನಿಮ್ಮ ಸ್ಥಳ (ಹವಾಮಾನ ಥೀಮ್ ಮತ್ತು ನೀರಾವರಿ ಸಲಹೆಗಾಗಿ)",
        "location_placeholder": "ನಿಮ್ಮ ನಗರ/ಸ್ಥಳ ನಮೂದಿಸಿ",
        "enter_location_hint": "ಹವಾಮಾನ ಆಧಾರಿತ ನೀರಾವರಿ ಸಲಹೆ ಮತ್ತು ಥೀಮ್ ನೋಡಲು ಮೇಲೆ ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ನಮೂದಿಸಿ.",
        "soil_button": "🌱 ಮಣ್ಣಿನ ತೇವಾಂಶ",
        "soil_eyebrow": "ಲೈವ್ ಸೆನ್ಸಾರ್ ಫೀಡ್",
        "moisture_label": "ತೇವಾಂಶ ಮಟ್ಟ",
        "soil_error": "ಮಣ್ಣಿನ ತೇವಾಂಶ ಡೇಟಾ ಸಿಗಲಿಲ್ಲ — ಸೆನ್ಸಾರ್ ಮತ್ತು ThingSpeak ಸಂಪರ್ಕವನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "weather_button": "🌦️ ನೀರಾವರಿ ಸಲಹೆ",
        "weather_eyebrow": "ಕ್ಷೇತ್ರ ಪರಿಸ್ಥಿತಿಗಳು",
        "weather_not_configured": "ಹವಾಮಾನ ವೈಶಿಷ್ಟ್ಯ ಕಾನ್ಫಿಗರ್ ಆಗಿಲ್ಲ — ಇದನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಲು ಆ್ಯಪ್ ಸೀಕ್ರೆಟ್ಸ್‌ನಲ್ಲಿ OpenWeatherMap API ಕೀ ಸೇರಿಸಿ.",
        "weather_error": "ಆ ಸ್ಥಳದ ಹವಾಮಾನ ಸಿಗಲಿಲ್ಲ — ಕಾಗುಣಿತ ಪರಿಶೀಲಿಸಿ ಅಥವಾ ಹತ್ತಿರದ ದೊಡ್ಡ ನಗರದ ಹೆಸರನ್ನು ಪ್ರಯತ್ನಿಸಿ.",
        "upload_label": "ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "uploaded_caption": "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಫೋಟೋ",
        "analyzing_eyebrow": "ಮಾದರಿ ವಿಶ್ಲೇಷಣೆ ನಡೆಯುತ್ತಿದೆ",
        "scan_line1": "ದೃಶ್ಯ ಲಕ್ಷಣಗಳನ್ನು ಹೊರತೆಗೆಯಲಾಗುತ್ತಿದೆ...",
        "scan_line2": "38 ಬೆಳೆ-ರೋಗ ಪ್ರೊಫೈಲ್‌ಗಳೊಂದಿಗೆ ಹೋಲಿಸಲಾಗುತ್ತಿದೆ...",
        "scan_line3": "ವಿಶ್ವಾಸ ಅಂಕವನ್ನು ಲೆಕ್ಕಹಾಕಲಾಗುತ್ತಿದೆ...",
        "diagnosis_eyebrow": "ರೋಗ ನಿರ್ಣಯ",
        "not_recognized_label": "⚠ ಬೆಳೆ ಗುರುತಿಸಲಾಗಲಿಲ್ಲ",
        "not_recognized_msg": "ಇದು ಬೆಂಬಲಿತ 14 ಬೆಳೆಗಳಲ್ಲಿ ({crops}) ಯಾವುದನ್ನೂ ಹೋಲುತ್ತಿಲ್ಲ. ವಿಶ್ವಾಸಾರ್ಹ ಫಲಿತಾಂಶಕ್ಕಾಗಿ ಈ ಬೆಳೆಗಳಲ್ಲಿ ಒಂದರ ಫೋಟೋ ಪ್ರಯತ್ನಿಸಿ.",
        "confidence_label": "ವಿಶ್ವಾಸ ಮಟ್ಟ",
        "confidence_note": "ವಿಶ್ವಾಸ ಮಟ್ಟ ಮಧ್ಯಮವಾಗಿದೆ — ಸ್ಪಷ್ಟವಾದ, ಚೆನ್ನಾಗಿ ಬೆಳಗಿದ ಒಂದೇ ಎಲೆಯ ಫೋಟೋ ನಿಖರತೆಯನ್ನು ಸುಧಾರಿಸಬಹುದು.",
        "treatment_eyebrow": "ಚಿಕಿತ್ಸಾ ಪ್ರೋಟೋಕಾಲ್",
        "what_means_header": "ಇದರ ಅರ್ಥವೇನು",
        "recommended_action_header": "ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮ",
        "web_search_button": "🌐 ಹೆಚ್ಚಿನ ಮಾಹಿತಿಗಾಗಿ ವೆಬ್ ಹುಡುಕಿ",
        "web_searching": "ಹೆಚ್ಚಿನ ಮಾಹಿತಿಗಾಗಿ ವೆಬ್ ಹುಡುಕಲಾಗುತ್ತಿದೆ...",
        "web_info_eyebrow": "ವೆಬ್‌ನಿಂದ ಹೆಚ್ಚಿನ ಮಾಹಿತಿ",
        "web_no_results": "ಯಾವುದೇ ವೆಬ್ ಫಲಿತಾಂಶಗಳು ಕಂಡುಬಂದಿಲ್ಲ — ಸ್ವಲ್ಪ ಸಮಯದ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "footer": "ಅಗ್ರೋ ಎಡ್ಜ್ // ಕ್ರಾಪ್ ಇಂಟೆಲಿಜೆನ್ಸ್ ಸಿಸ್ಟಮ್ // ಟೀಂ ಸೈಬರ್‌ಪಂಕ್",
        "last_updated": "ಕೊನೆಯದಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ:",
    },
    "ta": {
        "eyebrow_system": "// களக் கண்டறிதல் அமைப்பு",
        "hero_desc": "நோயைக் கண்டறிந்து சிகிச்சை ஆலோசனை பெற பயிர் இலையின் புகைப்படத்தை பதிவேற்றவும் — மேலும் உங்கள் இடத்திற்கான வானிலை அடிப்படையிலான பாசன ஆலோசனையும்.",
        "location_heading": "📍 உங்கள் இடம் (வானிலை தீம் & பாசன ஆலோசனைக்கு)",
        "location_placeholder": "உங்கள் நகரம்/இடத்தை உள்ளிடவும்",
        "enter_location_hint": "வானிலை அடிப்படையிலான பாசன ஆலோசனையையும் தீமையையும் காண மேலே உங்கள் இடத்தை உள்ளிடவும்.",
        "soil_button": "🌱 மண் ஈரப்பதம்",
        "soil_eyebrow": "நேரடி சென்சார் தரவு",
        "moisture_label": "ஈரப்பத நிலை",
        "soil_error": "மண் ஈரப்பத தரவு கிடைக்கவில்லை — சென்சார் மற்றும் ThingSpeak இணைப்பை சரிபார்க்கவும்.",
        "weather_button": "🌦️ பாசன ஆலோசனை",
        "weather_eyebrow": "வயல் நிலைமைகள்",
        "weather_not_configured": "வானிலை அம்சம் கட்டமைக்கப்படவில்லை — இதை இயக்க ஆப் சீக்ரெட்டுகளில் OpenWeatherMap API கீயைச் சேர்க்கவும்.",
        "weather_error": "அந்த இடத்திற்கான வானிலை கிடைக்கவில்லை — எழுத்துப்பிழையை சரிபார்க்கவும் அல்லது அருகிலுள்ள பெரிய நகரத்தின் பெயரை முயற்சிக்கவும்.",
        "upload_label": "இலையின் புகைப்படத்தை பதிவேற்றவும்",
        "uploaded_caption": "பதிவேற்றப்பட்ட புகைப்படம்",
        "analyzing_eyebrow": "மாதிரி பகுப்பாய்வு செய்யப்படுகிறது",
        "scan_line1": "காட்சி அம்சங்கள் பிரித்தெடுக்கப்படுகின்றன...",
        "scan_line2": "38 பயிர்-நோய் விவரக்குறிப்புகளுடன் ஒப்பிடப்படுகிறது...",
        "scan_line3": "நம்பகத்தன்மை மதிப்பெண் கணக்கிடப்படுகிறது...",
        "diagnosis_eyebrow": "நோய் கண்டறிதல்",
        "not_recognized_label": "⚠ பயிர் அடையாளம் காணப்படவில்லை",
        "not_recognized_msg": "இது ஆதரிக்கப்படும் 14 பயிர்களில் ({crops}) எதையும் ஒத்திருக்கவில்லை. நம்பகமான முடிவுக்கு இந்த பயிர்களில் ஒன்றின் புகைப்படத்தை முயற்சிக்கவும்.",
        "confidence_label": "நம்பகத்தன்மை",
        "confidence_note": "நம்பகத்தன்மை மிதமான அளவில் உள்ளது — தெளிவான, நல்ல வெளிச்சமுள்ள ஒரு இலையின் புகைப்படம் துல்லியத்தை மேம்படுத்தலாம்.",
        "treatment_eyebrow": "சிகிச்சை நெறிமுறை",
        "what_means_header": "இதன் பொருள் என்ன",
        "recommended_action_header": "பரிந்துரைக்கப்படும் நடவடிக்கை",
        "web_search_button": "🌐 மேலும் தகவலுக்கு இணையத்தில் தேடு",
        "web_searching": "மேலும் தகவலுக்காக இணையத்தில் தேடுகிறது...",
        "web_info_eyebrow": "இணையத்திலிருந்து கூடுதல் தகவல்",
        "web_no_results": "இணைய முடிவுகள் எதுவும் கிடைக்கவில்லை — சிறிது நேரம் கழித்து மீண்டும் முயற்சிக்கவும்.",
        "footer": "அக்ரோ எட்ஜ் // பயிர் நுண்ணறிவு அமைப்பு // டீம் சைபர்பங்க்",
        "last_updated": "கடைசியாக புதுப்பிக்கப்பட்டது:",
    },
}
 
 
@st.cache_data(show_spinner=False)
def translate_text(text, lang_code):
    """Translate dynamic model output (disease names, descriptions, treatments) into the target language."""
    if lang_code == "en" or not text:
        return text
    try:
        return GoogleTranslator(source="en", target=lang_code).translate(text)
    except Exception:
        return text
 
 
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
    transition: background-color 0.8s ease;
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
 
/* Location input label */
.loc-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-bottom: 0.3rem;
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
 
 
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("plant_model_v4.keras")
 
 
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
 
 
def get_weather_theme(condition_main):
    """Map an OpenWeatherMap 'main' condition to a color palette + background effect."""
    c = (condition_main or "").lower()
    if c in ("rain", "drizzle"):
        return {"bg": "#0A1620", "surface": "#101E29", "surface2": "#16283688",
                "accent": "#4FC3F7", "accent2": "#29B6F6", "glow": "rgba(79,195,247,0.28)",
                "effect": "rain"}
    if c == "thunderstorm":
        return {"bg": "#0A0A14", "surface": "#14141F", "surface2": "#1C1C2A",
                "accent": "#B39DDB", "accent2": "#7E57C2", "glow": "rgba(126,87,194,0.35)",
                "effect": "thunder"}
    if c == "snow":
        return {"bg": "#0E1618", "surface": "#161F22", "surface2": "#1E2A2E",
                "accent": "#E0F7FA", "accent2": "#80DEEA", "glow": "rgba(224,247,250,0.25)",
                "effect": "snow"}
    if c == "clear":
        return {"bg": "#140F06", "surface": "#1D160A", "surface2": "#271D0D",
                "accent": "#FFB74D", "accent2": "#FFD54F", "glow": "rgba(255,183,77,0.32)",
                "effect": "sun"}
    if c == "clouds":
        return {"bg": "#0D0F10", "surface": "#15181A", "surface2": "#1D2124",
                "accent": "#B0BEC5", "accent2": "#90A4AE", "glow": "rgba(176,190,197,0.2)",
                "effect": "clouds"}
    if c in ("mist", "fog", "haze", "smoke"):
        return {"bg": "#0F1210", "surface": "#171B18", "surface2": "#1F2620",
                "accent": "#CFD8DC", "accent2": "#B0BEC5", "glow": "rgba(207,216,220,0.18)",
                "effect": "fog"}
    return None
 
 
def render_weather_theme(theme):
    """Override root CSS variables and add an animated background effect matching the weather."""
    if not theme:
        return
 
    st.markdown(f"""
    <style>
    :root {{
        --bg: {theme['bg']};
        --surface: {theme['surface']};
        --surface-2: {theme['surface2']};
        --accent: {theme['accent']};
        --accent-2: {theme['accent2']};
        --glow: {theme['glow']};
    }}
    </style>
    """, unsafe_allow_html=True)
 
    effect = theme["effect"]
 
    if effect in ("rain", "thunder"):
        drops = ""
        for _ in range(30):
            left = random.uniform(0, 100)
            delay = random.uniform(0, 2)
            duration = random.uniform(0.6, 1.3)
            height = random.uniform(40, 80)
            drops += (f'<div class="raindrop" style="left:{left:.1f}%; height:{height:.0f}px; '
                      f'animation-delay:{delay:.2f}s; animation-duration:{duration:.2f}s;"></div>')
        flash_html = '<div class="lightning-flash"></div>' if effect == "thunder" else ""
        st.markdown(f"""
        <style>
        .weather-overlay {{ position: fixed; top:0; left:0; width:100%; height:100%;
            overflow:hidden; pointer-events:none; z-index:-1; }}
        .raindrop {{ position:absolute; top:-10%; width:1px;
            background:linear-gradient(to bottom, transparent, {theme['accent']});
            animation-name: rainFall; animation-timing-function: linear;
            animation-iteration-count: infinite; opacity:0.55; }}
        @keyframes rainFall {{ from {{ transform: translateY(-10vh); }} to {{ transform: translateY(110vh); }} }}
        .lightning-flash {{ position:fixed; top:0; left:0; width:100%; height:100%;
            background:#fff; opacity:0; animation: flash 7s infinite; pointer-events:none; z-index:999; }}
        @keyframes flash {{ 0%, 95%, 100% {{ opacity:0; }} 96% {{ opacity:0.55; }} 97% {{ opacity:0; }} 98% {{ opacity:0.3; }} }}
        </style>
        <div class="weather-overlay">{drops}</div>
        {flash_html}
        """, unsafe_allow_html=True)
 
    elif effect == "snow":
        flakes = ""
        for _ in range(24):
            left = random.uniform(0, 100)
            delay = random.uniform(0, 5)
            duration = random.uniform(4, 8)
            size = random.uniform(3, 7)
            flakes += (f'<div class="snowflake" style="left:{left:.1f}%; width:{size:.1f}px; height:{size:.1f}px; '
                       f'animation-delay:{delay:.2f}s; animation-duration:{duration:.2f}s;"></div>')
        st.markdown(f"""
        <style>
        .weather-overlay {{ position: fixed; top:0; left:0; width:100%; height:100%;
            overflow:hidden; pointer-events:none; z-index:-1; }}
        .snowflake {{ position:absolute; top:-5%; border-radius:50%; background:{theme['accent']};
            opacity:0.75; animation-name: snowFall; animation-timing-function: linear;
            animation-iteration-count: infinite; }}
        @keyframes snowFall {{ from {{ transform: translate(0, -10vh); }} to {{ transform: translate(24px, 110vh); }} }}
        </style>
        <div class="weather-overlay">{flakes}</div>
        """, unsafe_allow_html=True)
 
    elif effect == "sun":
        st.markdown(f"""
        <style>
        .weather-overlay {{ position: fixed; top:-25%; right:-15%; width:60vw; height:60vw;
            pointer-events:none; z-index:-1; border-radius:50%;
            background: radial-gradient(circle, {theme['glow']} 0%, transparent 70%);
            animation: sunPulse 4s ease-in-out infinite; }}
        @keyframes sunPulse {{ 0%,100% {{ opacity:0.75; }} 50% {{ opacity:1; }} }}
        </style>
        <div class="weather-overlay"></div>
        """, unsafe_allow_html=True)
 
    elif effect in ("clouds", "fog"):
        st.markdown(f"""
        <style>
        .weather-overlay {{ position: fixed; top:0; left:0; width:100%; height:100%;
            overflow:hidden; pointer-events:none; z-index:-1; }}
        .cloud-blob {{ position:absolute; border-radius:50%; background:{theme['glow']};
            filter: blur(30px); animation-name: cloudDrift; animation-timing-function: linear;
            animation-iteration-count: infinite; }}
        @keyframes cloudDrift {{ from {{ transform: translateX(-25vw); }} to {{ transform: translateX(125vw); }} }}
        </style>
        <div class="weather-overlay">
            <div class="cloud-blob" style="top:8%; width:220px; height:80px; animation-duration:38s;"></div>
            <div class="cloud-blob" style="top:28%; width:160px; height:60px; animation-duration:28s; animation-delay:-10s;"></div>
            <div class="cloud-blob" style="top:52%; width:260px; height:90px; animation-duration:45s; animation-delay:-20s;"></div>
        </div>
        """, unsafe_allow_html=True)
 
 
TRUSTED_PLANT_DOMAINS = [
    "extension.org", "apsnet.org", "plantvillage.psu.edu", "ipm.ucanr.edu",
    "rhs.org.uk", "gardeningknowhow.com", "planetnatural.com", "growveg.com",
    "cabi.org", "fao.org", "agriculture.com", "britannica.com", "wikipedia.org",
    "agrilinks.org", "agric.wa.gov.au", "almanac.com", "gardenia.net",
    "missouribotanicalgarden.org", "rhsgardening.org", "epicgardening.com",
    ".edu", ".gov", ".ac.in", ".edu.in",
]
 
 
@st.cache_data(show_spinner=False, ttl=3600)
def search_disease_info(query, max_results=3):
    """Search the web for extra info on a detected disease, biased toward plant/agriculture sources."""
    try:
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=max_results * 5))
        trusted = [r for r in raw_results if any(d in r.get("href", "").lower() for d in TRUSTED_PLANT_DOMAINS)]
        results = trusted[:max_results] if trusted else raw_results[:max_results]
        return results
    except Exception:
        return []
 
 
model = load_model()
 
# ---------------------------------------------------------------------------
# Language selector
# ---------------------------------------------------------------------------
lang_col, _ = st.columns([1, 2.5])
with lang_col:
    selected_lang_name = st.selectbox(
        "Language", list(LANGUAGES.keys()), label_visibility="collapsed"
    )
lang = LANGUAGES[selected_lang_name]
T = UI_STRINGS[lang]
 
# ---------------------------------------------------------------------------
# Location input — drives both the weather theme and the irrigation tip
# ---------------------------------------------------------------------------
st.markdown(f'<div class="loc-label">{T["location_heading"]}</div>', unsafe_allow_html=True)
city = st.text_input("Location", placeholder=T["location_placeholder"], label_visibility="collapsed")
 
weather_data = None
weather_configured = True
if city:
    api_key = st.secrets.get("OPENWEATHER_API_KEY", None)
    if not api_key:
        weather_configured = False
    else:
        weather_data = get_weather(city, api_key)
        if weather_data:
            theme = get_weather_theme(weather_data["weather"][0]["main"])
            render_weather_theme(theme)
 
# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
    <div class="hero-team">Team Cyberpunk</div>
    <div class="hero-eyebrow">{T['eyebrow_system']}</div>
    <h1>🌱 Agro Edge</h1>
    <p>{T['hero_desc']}</p>
</div>
""", unsafe_allow_html=True)
 
_, soil_col, weather_col = st.columns([2, 1, 1])
 
with soil_col:
    with st.popover(T["soil_button"], use_container_width=True):
        st.markdown(f'<div class="eyebrow">{T["soil_eyebrow"]}</div>', unsafe_allow_html=True)
        soil_data = get_soil_moisture()
        if soil_data and soil_data.get("field1") is not None:
            moisture = float(soil_data["field1"])
            timestamp = soil_data["created_at"]
            color = gauge_color(moisture)
 
            st.markdown(f"""
            <div class="gauge-wrap" style="margin-top:0.6rem;">
                <div class="gauge-label">
                    <span>{T['moisture_label']}</span>
                    <span class="gauge-value">{moisture:.0f}%</span>
                </div>
                <div class="gauge-track">
                    <div class="gauge-fill" style="width:{moisture:.0f}%; background:{color}; box-shadow: 0 0 12px {color}77;"></div>
                </div>
            </div>
            <p style="margin-top:0.9rem; font-size:0.8rem; color:var(--text-muted); font-family:'IBM Plex Mono', monospace;">{T['last_updated']} {timestamp}</p>
            """, unsafe_allow_html=True)
        else:
            st.warning(T["soil_error"])
 
with weather_col:
    with st.popover(T["weather_button"], use_container_width=True):
        st.markdown(f'<div class="eyebrow">{T["weather_eyebrow"]}</div>', unsafe_allow_html=True)
        if not city:
            st.info(T["enter_location_hint"])
        elif not weather_configured:
            st.info(T["weather_not_configured"])
        elif weather_data:
            temp = weather_data["main"]["temp"]
            condition = weather_data["weather"][0]["description"].title()
            tip = get_irrigation_tip(weather_data)
            condition_t = translate_text(condition, lang)
            tip_t = translate_text(tip, lang)
            st.markdown(f"""
            <div style="margin-top:0.6rem;">
                <p style="margin:0 0 0.4rem 0; font-weight:600; color:var(--text);">{city} — {condition_t}, {temp}°C</p>
                <p style="margin:0; font-size:0.92rem; color:var(--text);">{tip_t}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(T["weather_error"])
 
 
uploaded_file = st.file_uploader(T["upload_label"], type=["jpg", "jpeg", "png"])
 
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption=T["uploaded_caption"], use_container_width=True)
 
    # Preprocess exactly like training: resize to 224x224
    img_resized = image.resize((224, 224))
    img_array = np.array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)  # add batch dimension
 
    scan_placeholder = st.empty()
    scan_placeholder.markdown(f"""
    <div class="scan-card">
        <div class="eyebrow">{T['analyzing_eyebrow']}</div>
        <div class="scan-track"><div class="scan-bar"></div></div>
        <div class="scan-line">&gt; <span>{T['scan_line1']}</span></div>
        <div class="scan-line">&gt; <span>{T['scan_line2']}</span></div>
        <div class="scan-line">&gt; <span>{T['scan_line3']}</span></div>
    </div>
    """, unsafe_allow_html=True)
 
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = 100 * np.max(predictions[0])
 
    time.sleep(0.4)  # let the scan animation register before revealing the result
    scan_placeholder.empty()
 
    display_name = predicted_class.replace("___", " - ").replace("__", " ").replace("_", " ")
    display_name_t = translate_text(display_name, lang)
 
    if confidence < 70:
        not_recognized_msg_t = T["not_recognized_msg"].format(crops=SUPPORTED_CROPS)
        st.markdown(f"""
        <div class="card">
            <div class="eyebrow">{T['diagnosis_eyebrow']}</div>
            <div class="unrecognized">
                <div class="unrecognized-label">{T['not_recognized_label']}</div>
                {not_recognized_msg_t}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        color = gauge_color(confidence)
        confidence_note = "" if confidence >= 85 else f'<p style="margin-top:0.9rem; font-size:0.86rem; color:var(--text-muted);">{T["confidence_note"]}</p>'
 
        st.markdown(f"""
        <div class="card">
            <div class="eyebrow">{T['diagnosis_eyebrow']}</div>
            <div class="result-title">{display_name_t}</div>
            <div class="gauge-wrap">
                <div class="gauge-label">
                    <span>{T['confidence_label']}</span>
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
            description_t = translate_text(info["description"], lang)
            treatment_t = translate_text(info["treatment"], lang)
            st.markdown(f"""
            <div class="card">
                <div class="eyebrow">{T['treatment_eyebrow']}</div>
                <div class="rec-grid">
                    <div class="rec-box">
                        <h4>{T['what_means_header']}</h4>
                        <p>{description_t}</p>
                    </div>
                    <div class="rec-box treatment">
                        <h4>{T['recommended_action_header']}</h4>
                        <p>{treatment_t}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
 
        with st.spinner(T["web_searching"]):
            search_query = f"{display_name} plant disease symptoms causes treatment agriculture botany -software -app -company"
            web_results = search_disease_info(search_query)
        if web_results:
            st.markdown(f'<div class="card"><div class="eyebrow">{T["web_info_eyebrow"]}</div>', unsafe_allow_html=True)
            for r in web_results:
                title = r.get("title", "")
                link = r.get("href", "")
                body = r.get("body", "")[:200]
                title_t = translate_text(title, lang)
                body_t = translate_text(body, lang)
                st.markdown(f"""
                <div style="margin-bottom:0.9rem; padding-bottom:0.9rem; border-bottom:1px solid var(--border);">
                    <a href="{link}" target="_blank" style="color:var(--accent-2); font-weight:600; text-decoration:none; font-size:0.95rem;">{title_t}</a>
                    <p style="margin:0.3rem 0 0 0; font-size:0.85rem; color:var(--text-muted); line-height:1.5;">{body_t}...</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(T["web_no_results"])
 
st.markdown(f'<div class="sys-footer">{T["footer"]}</div>', unsafe_allow_html=True)
 
