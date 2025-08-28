from utils.logger import logger

def format_response(user_query, data, llm):
    """
    Format the OpenWeather API response into a human-readable message.
    """
    try:
        main = data.get("main", {})
        weather_list = data.get("weather", [{}])
        wind = data.get("wind", {})

        temperature = main.get("temp", "N/A")
        condition = weather_list[0].get("description", "N/A")
        humidity = main.get("humidity", "N/A")
        wind_speed = wind.get("speed", "N/A")

        city_name = data.get("name", "your location")

        response = f"""
Hey there! 👋

Current weather in {city_name}:

* Temperature: {temperature}°C 🌡️
* Condition: {condition} ☀️/☁️/🌧️
* Humidity: {humidity}% 💧
* Wind Speed: {wind_speed} m/s 💨
"""

        return response.strip()
    except Exception as e:
        return f"Could not format weather data: {e}"
