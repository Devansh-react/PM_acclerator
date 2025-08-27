from dotenv import load_dotenv

def format_response(user_query: str, weather_data: dict, llm):
    """
    Ask Gemini LLM to generate a detailed, human-friendly weather summary.
    Uses Gemini API key from .env via config.py.
    """

    prompt = f"""
    You are a helpful weather assistant. Your task is to generate a clear, conversational weather report for the user.

    Instructions:
    1. Start with a friendly greeting.
    2. Summarize the user's query: "{user_query}".
    3. Provide the current weather:
       - Include temperature, weather condition, humidity, and wind speed if available.
    4. Present a 5-day forecast:
       - For each day, list high and low temperatures, weather condition, and any notable events (rain, storms, etc.).
    5. Use bullet points or short paragraphs for readability.
    6. Avoid technical jargon; keep the language simple and engaging.
    7. End with a helpful tip or suggestion based on the forecast (e.g., "Don't forget your umbrella!").

    Weather Data:
    - Current: {weather_data.get('current')}
    - Forecast: {weather_data.get('forecast')}
    """

    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)
