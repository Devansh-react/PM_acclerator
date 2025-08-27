from fastapi import FastAPI
from pydantic import BaseModel
from graph.weather_graph import build_weather_graph
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from Schema.model import WeatherState
from utils.LLM_init import llm
from database.db import init_db

load_dotenv()
init_db()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherRequest(BaseModel):
    query: str

graph = build_weather_graph()

@app.get("/")
def root():
    return {"message": "Weather bot is running "}

@app.post("/get_weather")
def get_weather(req: WeatherRequest):
    print("📩 Incoming query:", req.query)   

    state: WeatherState = {
        "user_query": req.query,
        "llm": llm,
        "location": "",
        "weather_data": None,
        "from_cache": False,
        "final_answer": "",
        "error": ""
    }

    result = graph.invoke(state)

    print("📤 Graph result:", result)   
    return {"answer": result.get("final_answer", "")}