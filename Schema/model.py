from typing import TypedDict, Optional, Any

class WeatherState(TypedDict):
    user_query: str
    location: str
    weather_data: Optional[dict]
    from_cache: bool
    llm: Any
    final_answer: Optional[str]
    error: Optional[str]

