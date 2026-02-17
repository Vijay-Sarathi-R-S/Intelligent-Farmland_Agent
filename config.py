import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    NASA_API_KEY = os.getenv('NASA_API_KEY')
    
    # API Endpoints
    NASA_EARTH_API = "https://api.nasa.gov/planetary/earth/imagery"
    NASA_POWER_API = "https://power.larc.nasa.gov/api/power"
    OPEN_METEO_API = "https://archive-api.open-meteo.com/v1/archive"
    
    print("🔧 Config Loaded:")
    print(f"  - NASA API Key: {'✅ Present' if NASA_API_KEY else '❌ Missing'}")
    print(f"  - Gemini API Key: {'✅ Present' if GEMINI_API_KEY else '❌ Missing'}")