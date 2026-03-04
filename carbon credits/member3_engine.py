import os
from PIL import Image

class CarbonEstimationEngine:
    def __init__(self):
        self.buffer_percentage = 0.03
        self.carbon_price_per_credit = 800  # INR per credit

    def estimate_credits(self, land_area, practice_type, soil_type=None, yield_image=None):
        # Base credits for farming practice
        practice_credits = {'cover_crop': 1.2, 'no_till': 1.5, 'agroforestry': 2.0}
        base_credit = practice_credits.get(practice_type, 1.0)

        # Soil type adjustment
        soil_adjust = {'clay': 1.05, 'sandy': 0.95, 'loamy': 1.0}
        soil_factor = soil_adjust.get(soil_type, 1.0)

        # Yield image adjustment
        image_factor = 1.0
        if yield_image and os.path.exists(yield_image):
            try:
                img = Image.open(yield_image)
                image_factor += min(img.size[0], img.size[1]) / 10000
            except:
                pass

        # Compute credits
        raw_credits = land_area * base_credit * soil_factor * image_factor
        credits_after_buffer = raw_credits * (1 - self.buffer_percentage)
        estimated_income = credits_after_buffer * self.carbon_price_per_credit

        return {
            'land_area': land_area,
            'practice_type': practice_type,
            'soil_type': soil_type,
            'yield_image_reference': yield_image,
            'carbon_credits_after_buffer': round(credits_after_buffer, 2),
            'estimated_income': round(estimated_income, 2)
        }