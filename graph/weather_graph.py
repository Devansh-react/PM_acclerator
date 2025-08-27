from langgraph.graph import StateGraph, END
from tools.location_resolver import resolve_location
from database.cache import get_weather_cache, save_weather_cache
from tools.weather_api import fetch_weather
from tools.response_formatter import format_response
from orchestrator.state_manager import StateManager
from utils.logger import logger
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from Schema.model import WeatherState  # ensure this matches your schema
from utils.LLM_init import llm

load_dotenv()

# In-memory session cache
state_manager = StateManager()
CACHE_EXPIRY = timedelta(minutes=30)


# --------- NODE DEFINITIONS --------- #
def extract_location(state: WeatherState) -> WeatherState:
    """Extract location from user query."""
    query = state.get("user_query")
    location = resolve_location(query)

    if not location:
        logger.error("❌ Could not detect a location")
        return {**state, "error": "Could not detect a location."}

    return {**state, "location": location}


def check_cache(state: WeatherState) -> WeatherState:
    """Check in-memory and DB cache before calling API."""
    location = state["location"]

    # In-memory cache
    if state_manager.has_recent_weather(location, CACHE_EXPIRY):
        logger.info("🔄 Using in-memory cache")
        data = state_manager.get_weather(location)
        return {**state, "weather_data": data, "from_cache": True}

    # DB cache
    cached = get_weather_cache(location)
    if cached:
        ts = cached["timestamp"]
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)  # ensure datetime
        if datetime.now() - ts < CACHE_EXPIRY:
            logger.info("📦 Using DB cache")
            return {**state, "weather_data": cached["data"], "from_cache": True}

    # No cache
    return {**state, "weather_data": None, "from_cache": False}


def fetch_from_api(state: WeatherState) -> WeatherState:
    """Fetch weather from OpenWeather if not cached."""
    if state["weather_data"] is not None:
        return state  # already resolved

    location = state["location"]
    logger.info(f"🌍 Fetching weather from API for {location}")

    data = fetch_weather(location)
    save_weather_cache(location, data)
    state_manager.update_weather(location, data)

    return {**state, "weather_data": data}


def format_answer(state: WeatherState) -> WeatherState:
    """Format final answer with LLM or return error."""
    if "error" in state:
        return {**state, "final_answer": state["error"]}

    query = state["user_query"]
    data = state["weather_data"]
    llm = state["llm"]

    answer = format_response(query, data, llm)
    return {**state, "final_answer": answer}


# --------- GRAPH DEFINITION --------- #
def build_weather_graph():
    workflow = StateGraph(WeatherState)

    # Nodes
    workflow.add_node("extract_location", extract_location)
    workflow.add_node("check_cache", check_cache)
    workflow.add_node("fetch_from_api", fetch_from_api)
    workflow.add_node("format_answer", format_answer)

    # Flow:
    workflow.set_entry_point("extract_location")

    # If error in location → jump straight to format_answer
    workflow.add_conditional_edges(
        "extract_location",
        lambda state: "error" in state,
        {
            True: "format_answer",
            False: "check_cache"
        }
    )

    # Normal flow
    workflow.add_edge("check_cache", "fetch_from_api")
    workflow.add_edge("fetch_from_api", "format_answer")
    workflow.add_edge("format_answer", END)

    return workflow.compile()


# --------- RUNNER --------- #
if __name__ == "__main__":
    graph = build_weather_graph()

    while True:
        query = input("\nAsk about the weather (or 'quit'): ")
        if query.lower() in ["quit", "exit"]:
            break

        state: WeatherState = {
            "user_query": query,
            "llm": llm,
            "location": "",
            "weather_data": None,
            "from_cache": False,
            "final_answer": "",
            "error": ""
        }
        result = graph.invoke(state)
        print("\n🤖:", result["final_answer"])
