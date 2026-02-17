class AgriculturalKnowledgeBase:

    def __init__(self):

        # =========================================
        # CROP DATABASE (RAG STATIC KNOWLEDGE)
        # =========================================
        self.crops = {
            "rice": {
                "temperature": {"min": 20, "max": 35},
                "rainfall": {"min": 1200, "max": 3000}
            },
            "maize": {
                "temperature": {"min": 18, "max": 35},
                "rainfall": {"min": 500, "max": 1200}
            },
            "wheat": {
                "temperature": {"min": 10, "max": 30},
                "rainfall": {"min": 300, "max": 1000}
            },
            "cotton": {
                "temperature": {"min": 20, "max": 38},
                "rainfall": {"min": 500, "max": 1000}
            },
            "groundnut": {
                "temperature": {"min": 20, "max": 35},
                "rainfall": {"min": 500, "max": 1200}
            }
        }

    # ==================================================
    # Get crop requirements
    # ==================================================
    def get_crop_requirements(self, crop_name):

        if not crop_name:
            return None

        return self.crops.get(crop_name.lower())

    # ==================================================
    # Calculate Suitability Score
    # ==================================================
    def get_crop_suitability_score(self, crop, temp, monthly_rain):

        crop_data = self.get_crop_requirements(crop)
        if not crop_data:
            return {"score": 0}

        annual_rain = monthly_rain * 12

        temp_ok = crop_data["temperature"]["min"] <= temp <= crop_data["temperature"]["max"]
        rain_ok = crop_data["rainfall"]["min"] <= annual_rain <= crop_data["rainfall"]["max"]

        score = 0
        if temp_ok:
            score += 0.5
        if rain_ok:
            score += 0.5

        return {
            "score": score,
            "temperature_status": "Optimal" if temp_ok else "Unsuitable",
            "rainfall_status": "Optimal" if rain_ok else "Unsuitable"
        }

    # ==================================================
    # Recommend Crops by Conditions
    # ==================================================
    def search_crops_by_conditions(self, temp, monthly_rain):

        annual_rain = monthly_rain * 12
        suitable = []

        for crop, data in self.crops.items():

            if (
                data["temperature"]["min"] <= temp <= data["temperature"]["max"]
                and
                data["rainfall"]["min"] <= annual_rain <= data["rainfall"]["max"]
            ):
                suitable.append(crop)

        return suitable
