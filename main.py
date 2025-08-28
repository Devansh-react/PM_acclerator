from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Schema.model import WeatherState
from utils.LLM_init import llm
from tools.location_resolver import resolve_location
from database.cache import get_weather_cache, save_weather_cache
from orchestrator.state_manager import StateManager
from tools.response_formatter import format_response
from langgraph.graph import StateGraph, END
import requests
import re
import os
import logging

load_dotenv()


API_KEY = os.getenv("OPENWEATHER_API_KEY")
CACHE_EXPIRY = timedelta(minutes=30)
state_manager = StateManager()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    user_query: str

def get_coordinates(location: str):
    """Resolve location string to latitude/longitude using OpenWeather Geocoding API."""
    # Direct geocoding
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": location, "limit": 1, "appid": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    if data:
        return data[0]["lat"], data[0]["lon"]


    url_zip = "http://api.openweathermap.org/geo/1.0/zip"
    params_zip = {"zip": location, "appid": API_KEY}
    response_zip = requests.get(url_zip, params=params_zip)
    data_zip = response_zip.json()
    if "lat" in data_zip and "lon" in data_zip:
        return data_zip["lat"], data_zip["lon"]


    match = re.match(r"^\s*([-\d\.]+)\s*,\s*([-\d\.]+)\s*$", location)
    if match:
        return float(match.group(1)), float(match.group(2))

    return None, None

def fetch_weather(location: str):
    """Fetch current weather data using coordinates."""
    lat, lon = get_coordinates(location)
    if lat is None or lon is None:
        return {"error": f"Could not resolve location: {location}"}

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def extract_location(state: WeatherState) -> WeatherState:
    query = state.get("user_query")
    location = resolve_location(query, state["llm"])
    if not location:
        logger.error("❌ Could not detect a location")
        return {**state, "error": "Could not detect a location."}
    return {**state, "location": location}

def check_cache(state: WeatherState) -> WeatherState:
    location = state["location"]


    if state_manager.has_recent_weather(location, CACHE_EXPIRY):
        logger.info("🔄 Using in-memory cache")
        data = state_manager.get_weather(location)
        return {**state, "weather_data": data, "from_cache": True}


    cached = get_weather_cache(location)
    if cached:
        ts = cached["timestamp"]
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts)
            except ValueError:
                ts = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - ts < CACHE_EXPIRY:
            logger.info("📦 Using DB cache")
            return {**state, "weather_data": cached["data"], "from_cache": True}

    return {**state, "weather_data": None, "from_cache": False}

def fetch_from_api(state: WeatherState) -> WeatherState:
    if state["weather_data"] is not None:
        return state
    
    location = state["location"]
    logger.info(f"🌍 Fetching weather from API for {location}")
    data = fetch_weather(location)
    
    if "error" in data:
        logger.error(f"❌ {data['error']}")
        return {**state, "error": data["error"]}

    save_weather_cache(location, data)
    state_manager.update_weather(location, data)
    logger.info(f"✅ Weather data fetched from API: {data}")
    return {**state, "weather_data": data}

def format_answer(state: WeatherState) -> WeatherState:
    if state.get("error"):
        logger.error(f"❌ Error in state: {state['error']}")
        return {**state, "final_answer": state["error"]}

    query = state["user_query"]
    data = state["weather_data"]
    logger.info(f"📝 Formatting answer with data: {data}")

    if not data:
        return {**state, "final_answer": "No weather data available."}

    llm_inst = state["llm"]
    answer = format_response(query, data, llm_inst)
    logger.info(f"🤖 LLM answer: {answer}")

    return {**state, "final_answer": answer or "I couldn’t generate a response."}

def build_weather_graph():
    workflow = StateGraph(WeatherState)

    workflow.add_node("extract_location", extract_location)
    workflow.add_node("check_cache", check_cache)
    workflow.add_node("fetch_from_api", fetch_from_api)
    workflow.add_node("format_answer", format_answer)

    workflow.set_entry_point("extract_location")

    workflow.add_conditional_edges(
        "extract_location",
        lambda state: bool(state.get("error")),
        {True: "format_answer", False: "check_cache"}
    )

    workflow.add_edge("check_cache", "fetch_from_api")
    workflow.add_edge("fetch_from_api", "format_answer")
    workflow.add_edge("format_answer", END)

    return workflow.compile()

graph = build_weather_graph()


@app.post("/weather")
def get_weather(query: Query):
    state: WeatherState = {
        "user_query": query.user_query,
        "llm": llm,
        "location": "",
        "weather_data": None,
        "from_cache": False,
        "final_answer": "",
        "error": ""
    }
    result = graph.invoke(state)
    return result
