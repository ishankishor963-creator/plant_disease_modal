"""
Disease recommendation dictionary.
Maps each model class name (exactly as produced by the PlantVillage folder names)
to a short description and a practical treatment/management tip.
"""

RECOMMENDATIONS = {
    "Pepper__bell___Bacterial_spot": {
        "description": "A bacterial disease causing small, dark, water-soaked spots on leaves and fruit, which can lead to defoliation and reduced yield.",
        "treatment": "Remove and destroy infected plant debris. Avoid overhead watering to reduce leaf wetness. Apply copper-based bactericides early, and rotate crops (avoid planting peppers/tomatoes in the same soil for 2-3 years)."
    },
    "Pepper__bell___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Potato___Early_blight": {
        "description": "A fungal disease (Alternaria solani) causing dark concentric 'target-spot' lesions on older leaves first, which can spread and reduce tuber yield.",
        "treatment": "Remove infected lower leaves, avoid overhead irrigation, ensure good air circulation between plants, and apply a fungicide containing chlorothalonil or mancozeb if the infection is spreading."
    },
    "Potato___Late_blight": {
        "description": "A fast-spreading, highly destructive fungal-like disease (Phytophthora infestans) causing dark, water-soaked blotches on leaves that can destroy a crop within days in wet, cool weather.",
        "treatment": "Act quickly: remove and destroy infected plants, avoid working in wet fields (spreads spores), and apply a fungicide with chlorothalonil or copper-based compounds. Improve field drainage and spacing for airflow."
    },
    "Potato___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Tomato_Bacterial_spot": {
        "description": "A bacterial disease causing small, dark, greasy-looking spots on leaves and fruit, thriving in warm, humid conditions.",
        "treatment": "Avoid overhead watering and working with wet plants. Remove infected debris. Apply copper-based sprays early, and use disease-free seed/transplants next season."
    },
    "Tomato_Early_blight": {
        "description": "A fungal disease causing dark, concentric-ringed spots on older leaves first, eventually leading to yellowing and leaf drop.",
        "treatment": "Prune lower leaves touching soil, mulch to prevent soil splash, ensure good airflow, and apply a fungicide (chlorothalonil or mancozeb) if spreading. Rotate crops each season."
    },
    "Tomato_Late_blight": {
        "description": "A fast-spreading disease (Phytophthora infestans) causing large, water-soaked, grey-green blotches on leaves and stems, especially damaging in cool, wet weather.",
        "treatment": "Remove and destroy infected plants immediately. Avoid overhead irrigation. Apply fungicides containing chlorothalonil or copper preventively during humid weather, and space plants for good airflow."
    },
    "Tomato_Leaf_Mold": {
        "description": "A fungal disease common in humid environments, causing pale yellow spots on the upper leaf surface and olive-green mold underneath.",
        "treatment": "Improve ventilation (especially in greenhouses/tunnels), reduce humidity around plants, avoid wetting leaves when watering, and apply a fungicide if the infection persists."
    },
    "Tomato_Septoria_leaf_spot": {
        "description": "A fungal disease causing small, circular spots with dark borders and grey centers on lower leaves, which can spread upward and cause defoliation.",
        "treatment": "Remove infected lower leaves, mulch around the base to prevent soil splash, avoid overhead watering, and apply a fungicide (chlorothalonil-based) if it continues to spread."
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "description": "Tiny pests (not a disease) that cause stippled, yellowing leaves and fine webbing, thriving in hot, dry conditions.",
        "treatment": "Spray plants with water to dislodge mites, apply insecticidal soap or neem oil, and introduce natural predators like ladybugs if possible. Avoid drought stress on plants, which attracts mites."
    },
    "Tomato__Target_Spot": {
        "description": "A fungal disease causing small brown spots with concentric rings on leaves, stems, and fruit, which can be confused with early blight or bacterial spot.",
        "treatment": "Remove infected leaves and debris, avoid overhead watering, ensure good spacing/airflow, and apply a fungicide (chlorothalonil or azoxystrobin) if the infection spreads."
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "description": "A viral disease transmitted by whiteflies, causing upward leaf curling, yellowing, and stunted growth. There is no cure once infected.",
        "treatment": "Remove and destroy infected plants to prevent spread. Control whitefly populations with yellow sticky traps and neem oil or insecticidal spray. Use resistant tomato varieties in future plantings."
    },
    "Tomato__Tomato_mosaic_virus": {
        "description": "A viral disease causing mottled light and dark green patterns on leaves, along with stunted growth and reduced fruit quality.",
        "treatment": "Remove and destroy infected plants immediately (virus has no cure). Disinfect tools between plants, wash hands before handling plants, and avoid tobacco product contact with plants (virus can spread this way). Use resistant varieties next season."
    },
    "Tomato_healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
}
