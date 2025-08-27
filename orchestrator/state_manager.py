from datetime import datetime

class StateManager:
    """
    Manages short-term in-memory cache for weather data.
    Helps avoid repeated DB/API calls in the same conversation.
    """

    def __init__(self):
        self.weather_state = {}

    def update_weather(self, location: str, data: dict):
        self.weather_state[location] = {"data": data, "timestamp": datetime.now()}

    def has_recent_weather(self, location: str, expiry) -> bool:
        if location not in self.weather_state:
            return False
        last = self.weather_state[location]["timestamp"]
        return (datetime.now() - last) < expiry

    def get_weather(self, location: str) -> dict:
        return self.weather_state.get(location, {}).get("data")
