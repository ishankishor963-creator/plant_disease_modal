
"""
Disease recommendation dictionary.
Maps each model class name (exactly as produced by the PlantVillage "color" folder names)
to a short description and a practical treatment/management tip.
Covers 38 classes across 14 crops: apple, blueberry, cherry, corn, grape, orange,
peach, pepper, potato, raspberry, soybean, squash, strawberry, tomato.
"""

RECOMMENDATIONS = {
    "Apple___Apple_scab": {
        "description": "A fungal disease causing dark, scabby, olive-green to black spots on leaves and fruit, common in cool, wet spring weather.",
        "treatment": "Rake and destroy fallen leaves in autumn to reduce overwintering spores. Prune for better airflow, and apply a fungicide (captan or myclobutanil) starting at bud break if the disease is recurring."
    },
    "Apple___Black_rot": {
        "description": "A fungal disease causing purple-bordered leaf spots and rotting, mummified fruit, often entering through wounds or dead wood.",
        "treatment": "Prune out dead or cankered wood and remove mummified fruit from the tree and ground. Apply a fungicide (captan or thiophanate-methyl) during the growing season if infection is active."
    },
    "Apple___Cedar_apple_rust": {
        "description": "A fungal disease requiring both apple and juniper/cedar trees to complete its life cycle, causing bright orange-yellow spots on apple leaves.",
        "treatment": "Remove nearby juniper/cedar hosts if possible, or accept some distance won't fully stop wind-blown spores. Apply a protective fungicide (myclobutanil or copper-based) starting at bud break and continuing through spring."
    },
    "Apple___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Blueberry___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "description": "A fungal disease causing a white, powdery coating on leaves and shoots, thriving in warm, dry conditions with high humidity.",
        "treatment": "Improve air circulation with proper pruning, avoid excess nitrogen fertilizer, and apply a sulfur-based or potassium bicarbonate fungicide if the infection spreads."
    },
    "Cherry_(including_sour)___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "description": "A fungal disease causing rectangular, grey-brown lesions on corn leaves, which can significantly reduce yield in severe cases.",
        "treatment": "Rotate crops away from corn for at least one season, till under infected residue, choose resistant hybrids where possible, and apply a fungicide (strobilurin or triazole-based) if the infection is severe."
    },
    "Corn_(maize)___Common_rust_": {
        "description": "A fungal disease causing small, reddish-brown, powdery pustules on both leaf surfaces.",
        "treatment": "Most modern corn hybrids have good resistance; if severe, apply a fungicide (strobilurin-based). Rotate crops and avoid dense planting that limits airflow."
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "description": "A fungal disease causing long, cigar-shaped grey-green to tan lesions on leaves, which can merge and kill large areas of foliage.",
        "treatment": "Use resistant hybrids where available, rotate crops, till under infected residue, and apply a fungicide (strobilurin or triazole-based) if detected early in susceptible fields."
    },
    "Corn_(maize)___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Grape___Black_rot": {
        "description": "A fungal disease causing circular brown leaf spots and shriveled, mummified fruit that turns black.",
        "treatment": "Remove mummified fruit and infected leaves/canes during dormant pruning. Apply a fungicide (mancozeb or myclobutanil) starting early in the season, especially during wet weather."
    },
    "Grape___Esca_(Black_Measles)": {
        "description": "A complex fungal trunk disease causing striped, discolored leaves and dark spotting on fruit; can lead to sudden vine collapse in severe cases.",
        "treatment": "There is no full cure — prune out and destroy infected wood during dry weather to reduce spread, avoid pruning wounds during wet conditions, and maintain overall vine health to slow progression."
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "description": "A fungal disease causing angular brown spots on leaves that can lead to premature defoliation.",
        "treatment": "Remove fallen infected leaves, improve canopy airflow through pruning, and apply a fungicide (mancozeb or copper-based) if the infection is spreading."
    },
    "Grape___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "description": "A serious bacterial disease spread by psyllid insects, causing yellowing/mottled leaves, lopsided bitter fruit, and eventual tree decline. There is no cure.",
        "treatment": "Remove and destroy infected trees to prevent spread. Control psyllid populations with recommended insecticides or biological controls, and plant only certified disease-free nursery stock going forward."
    },
    "Peach___Bacterial_spot": {
        "description": "A bacterial disease causing small, dark, water-soaked spots on leaves and fruit, which can lead to leaf drop and fruit blemishes.",
        "treatment": "Prune for good airflow, avoid overhead irrigation, and apply copper-based bactericides during dormant season and early growing season if the disease is recurring."
    },
    "Peach___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Pepper,_bell___Bacterial_spot": {
        "description": "A bacterial disease causing small, dark, water-soaked spots on leaves and fruit, which can lead to defoliation and reduced yield.",
        "treatment": "Remove and destroy infected plant debris. Avoid overhead watering to reduce leaf wetness. Apply copper-based bactericides early, and rotate crops (avoid planting peppers/tomatoes in the same soil for 2-3 years)."
    },
    "Pepper,_bell___healthy": {
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
    "Raspberry___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Soybean___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Squash___Powdery_mildew": {
        "description": "A fungal disease causing a white, powdery coating on leaves and stems, common in warm weather with high humidity.",
        "treatment": "Improve air circulation with proper spacing, avoid overhead watering, and apply a sulfur-based, potassium bicarbonate, or neem oil fungicide if the infection spreads."
    },
    "Strawberry___Leaf_scorch": {
        "description": "A fungal disease causing small purple spots on leaves that enlarge and give a scorched, dried appearance.",
        "treatment": "Remove and destroy infected leaves after harvest, avoid overhead watering, ensure good spacing for airflow, and apply a fungicide (captan-based) if the infection is severe."
    },
    "Strawberry___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
    "Tomato___Bacterial_spot": {
        "description": "A bacterial disease causing small, dark, greasy-looking spots on leaves and fruit, thriving in warm, humid conditions.",
        "treatment": "Avoid overhead watering and working with wet plants. Remove infected debris. Apply copper-based sprays early, and use disease-free seed/transplants next season."
    },
    "Tomato___Early_blight": {
        "description": "A fungal disease causing dark, concentric-ringed spots on older leaves first, eventually leading to yellowing and leaf drop.",
        "treatment": "Prune lower leaves touching soil, mulch to prevent soil splash, ensure good airflow, and apply a fungicide (chlorothalonil or mancozeb) if spreading. Rotate crops each season."
    },
    "Tomato___Late_blight": {
        "description": "A fast-spreading disease (Phytophthora infestans) causing large, water-soaked, grey-green blotches on leaves and stems, especially damaging in cool, wet weather.",
        "treatment": "Remove and destroy infected plants immediately. Avoid overhead irrigation. Apply fungicides containing chlorothalonil or copper preventively during humid weather, and space plants for good airflow."
    },
    "Tomato___Leaf_Mold": {
        "description": "A fungal disease common in humid environments, causing pale yellow spots on the upper leaf surface and olive-green mold underneath.",
        "treatment": "Improve ventilation (especially in greenhouses/tunnels), reduce humidity around plants, avoid wetting leaves when watering, and apply a fungicide if the infection persists."
    },
    "Tomato___Septoria_leaf_spot": {
        "description": "A fungal disease causing small, circular spots with dark borders and grey centers on lower leaves, which can spread upward and cause defoliation.",
        "treatment": "Remove infected lower leaves, mulch around the base to prevent soil splash, avoid overhead watering, and apply a fungicide (chlorothalonil-based) if it continues to spread."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "description": "Tiny pests (not a disease) that cause stippled, yellowing leaves and fine webbing, thriving in hot, dry conditions.",
        "treatment": "Spray plants with water to dislodge mites, apply insecticidal soap or neem oil, and introduce natural predators like ladybugs if possible. Avoid drought stress on plants, which attracts mites."
    },
    "Tomato___Target_Spot": {
        "description": "A fungal disease causing small brown spots with concentric rings on leaves, stems, and fruit, which can be confused with early blight or bacterial spot.",
        "treatment": "Remove infected leaves and debris, avoid overhead watering, ensure good spacing/airflow, and apply a fungicide (chlorothalonil or azoxystrobin) if the infection spreads."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "description": "A viral disease transmitted by whiteflies, causing upward leaf curling, yellowing, and stunted growth. There is no cure once infected.",
        "treatment": "Remove and destroy infected plants to prevent spread. Control whitefly populations with yellow sticky traps and neem oil or insecticidal spray. Use resistant tomato varieties in future plantings."
    },
    "Tomato___Tomato_mosaic_virus": {
        "description": "A viral disease causing mottled light and dark green patterns on leaves, along with stunted growth and reduced fruit quality.",
        "treatment": "Remove and destroy infected plants immediately (virus has no cure). Disinfect tools between plants, wash hands before handling plants, and avoid tobacco product contact with plants (virus can spread this way). Use resistant varieties next season."
    },
    "Tomato___healthy": {
        "description": "No disease detected. The plant appears healthy.",
        "treatment": "Continue regular monitoring, balanced fertilization, and consistent watering. No treatment needed."
    },
}
