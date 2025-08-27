from database.cache import get_weather_cache, save_weather_cache
from tools.weather_api import fetch_weather
from tools.location_resolver import resolve_location
from tools.response_formatter import format_response
from utils.logger import logger
from datetime import datetime, timedelta
from orchestrator.state_manager import StateManager

CACHE_EXPIRY = timedelta(minutes=30)

state_manager = StateManager()

def orchestrate(user_query, llm):
    # Step 1: Extract location
    location = resolve_location(user_query)
    if not location:
        return "I couldn't detect a location. Please specify one."

    # Step 2: Check session state (avoid repeated calls in the same conversation)
    if state_manager.has_recent_weather(location, CACHE_EXPIRY):
        logger.info("🔄 Using in-memory cached weather data")
        weather_data = state_manager.get_weather(location)
    else:
        # Step 3: Check DB cache
        cached = get_weather_cache(location)
        if cached and datetime.now() - cached["timestamp"] < CACHE_EXPIRY:
            logger.info("📦 Using DB cached weather data")
            weather_data = cached["data"]
        else:
            # Step 4: Fetch from API
            logger.info("🌍 Fetching fresh weather data")
            weather_data = fetch_weather(location)
            save_weather_cache(location, weather_data)

        # Update in-memory session state
        state_manager.update_weather(location, weather_data)

    # Step 5: Pass through LLM for formatting
    return format_response(user_query, weather_data, llm)
