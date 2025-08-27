def kelvin_to_celsius(k: float) -> float:
    return round(k - 273.15, 1)

def kelvin_to_fahrenheit(k: float) -> float:
    return round((k - 273.15) * 9/5 + 32, 1)

def format_temp(temp_c: float) -> str:
    return f"{temp_c}°C"
