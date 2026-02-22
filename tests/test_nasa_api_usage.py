import os
import requests
from dotenv import load_dotenv

# Load .env from project root
load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

def test_nasa_api_usage():
    assert NASA_API_KEY is not None, "NASA_API_KEY not found in .env"

    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": NASA_API_KEY
    }

    response = requests.get(url, params=params)

    # Check status
    assert response.status_code == 200, f"NASA API error: {response.text}"

    # Print rate limit info (visible when running pytest -s)
    print("\nNASA API Rate Limits:")
    print("Limit:", response.headers.get("X-RateLimit-Limit"))
    print("Remaining:", response.headers.get("X-RateLimit-Remaining"))

    # Basic validation
    data = response.json()
    assert "date" in data, "Unexpected response from NASA API"
