import requests
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5"

def fetch_weather(location: str) -> dict:
    """
    Fetch current weather + 5-day forecast from OpenWeather API.
    Uses API key from .env (via config.py).
    """
    if not load_dotenv.OPENWEATHER_API_KEY:
        raise ValueError("❌ OpenWeather API key not set in environment")

    params = {"q": location, "appid": load_dotenv.OPENWEATHER_API_KEY, "units": "metric"}

    # Current weather
    r = requests.get(f"{BASE_URL}/weather", params=params)
    r.raise_for_status()
    current = r.json()

    # 5-day forecast
    f = requests.get(f"{BASE_URL}/forecast", params=params)
    f.raise_for_status()
    forecast = f.json()

    logger.info(f"✅ Weather data fetched for {location}")
    return {"current": current, "forecast": forecast}
