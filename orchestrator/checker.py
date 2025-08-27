from database.cache import get_weather_cache, save_weather_cache
from tools.weather_api import fetch_weather
from tools.location_resolver import resolve_location
from utils.logger import logger
from datetime import datetime, timedelta
from orchestrator.state_manager import StateManager


CACHE_EXPIRY = timedelta(minutes=30)
state_manager = StateManager()


def orchestrate(user_query, llm):

    location = resolve_location(user_query, llm)
    if not location:
        return "couldn't detect a location"


    if state_manager.has_recent_weather(location, CACHE_EXPIRY):
        logger.info("Using in-memory cached weather data")
        weather_data = state_manager.get_weather(location)
    else:
   
        cached = get_weather_cache(location)
        if cached:
            ts = cached["timestamp"]
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except ValueError:
                    ts = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") 

            if datetime.now() - ts < CACHE_EXPIRY:
                logger.info("Using DB cached weather data")
                weather_data = cached["data"]
            else:
                logger.info("Fetching fresh weather data (cache expired)")
                weather_data = fetch_weather(location)
                save_weather_cache(location, weather_data)
        else:
            
            logger.info("Fetching fresh weather data (no cache)")
            weather_data = fetch_weather(location)  
            save_weather_cache(location, weather_data)

        state_manager.update_weather(location, weather_data)
    return weather_data
