from member3_engine import CarbonEstimationEngine

engine = CarbonEstimationEngine()

sample_data = {
    "land_area": 5,
    "practice_type": "cover_crop",
    "soil_type": "clay",
    "yield_image": "images/yield1.jpg"
}

result = engine.estimate_credits(**sample_data)
print("------ SAMPLE OUTPUT ------")
print(result)