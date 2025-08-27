from utils.logger import logger

def format_response(user_query: str, weather_data: dict, llm):
    """
    Format weather response using LLM if available, else fallback.
    """
    try:
        logger.info(f"📝 Formatting response for city: {user_query}")

        city = weather_data.get("city", "Unknown")
        country = weather_data.get("country", "")
        temp = weather_data.get("temperature", "N/A")
        desc = weather_data.get("description", "N/A")
        humidity = weather_data.get("humidity", "N/A")
        wind = weather_data.get("wind_speed", "N/A")

        base_response = (
            f"Weather in {city}, {country}:\n"
            f"- Temperature: {temp}°C\n"
            f"- Condition: {desc}\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind Speed: {wind} m/s"
        )

        if llm:
            try:
                prompt = f"""
                User asked: "{user_query}"

                Here is the weather data:
                - City: {city}, {country}
                - Temperature: {temp}°C
                - Condition: {desc}
                - Humidity: {humidity}%
                - Wind Speed: {wind} m/s

                Format the answer in a **friendly, clear style** with emojis and line breaks.  
                Keep it short and readable, like a weather app update.
                """

                response = llm.invoke(prompt)  # ✅ works with ChatGoogleGenerativeAI
                return response.content if hasattr(response, "content") else str(response)
            except Exception as e:
                logger.error(f"⚠️ LLM formatting failed: {e}")
                return base_response

        return base_response

    except Exception as e:
        logger.error(f"⚠️ Error in format_response: {e}")
        return "Sorry, I couldn’t format the weather data properly."
