import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_coordinates(location: str):
    """Use OpenWeather Geocoding API to get latitude and longitude for a location string."""
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": location,
        "limit": 1,      # get only the top match
        "appid": API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    if not data:
        raise ValueError(f"Could not find coordinates for location: {location}")
    
    return data[0]["lat"], data[0]["lon"]

def fetch_weather(location: str):
    """Fetch current weather for a location string using coordinates."""
    try:
        lat, lon = get_coordinates(location)
    except ValueError as e:
        return {"error": str(e)}
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"   # or 'imperial'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Example usage
user_input = "newyork"  # whatever the LLM extracted
weather_data = fetch_weather(user_input)
print(weather_data)
