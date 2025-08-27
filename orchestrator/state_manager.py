from datetime import datetime, timedelta

class StateManager:
    def __init__(self):
        # Stores weather data as { location: (timestamp, weather_data_dict) }
        self.session_state = {}

    def has_recent_weather(self, location: str, expiry: timedelta) -> bool:
        """Check if we have recent weather for a location."""
        if location not in self.session_state:
            return False

        ts, _ = self.session_state[location]
        return datetime.now() - ts < expiry

    def get_weather(self, location: str):
        """Retrieve cached weather data (dict) if available."""
        if location in self.session_state:
            _, data = self.session_state[location]
            return data
        return None

    def update_weather(self, location: str, weather_data: dict):
        """Update in-memory cache with latest weather data (dict)."""
        self.session_state[location] = (datetime.now(), weather_data)
