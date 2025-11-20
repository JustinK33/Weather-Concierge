import os
import requests

def get_weather(city: str) -> str:
    """Look up the current weather for a given city using OpenWeatherMap and return a short human-readable description."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather service not configured (missing api key)"
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    parameters = {
        "q": city,
        "appid": api_key,
        "units": "imperial",
    }
    try:
        resp = requests.get(url, params=parameters, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        return f"Error calling weather API: {e}"

    data = resp.json()
    try:
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
    except (KeyError, IndexError):
        return f"Couldn't parse weather data for '{city}'."

    return (
        f"In {city}, it's currently {description}, "
        f"{temp:.1f}°C (feels like {feels_like:.1f}°C)."
    )