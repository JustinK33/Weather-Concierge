# app/tools/weather.py
import os
import requests
from typing import Any, Dict, List
from langchain.tools import tool

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

def _ensure_key() -> str:
    if not WEATHER_API_KEY:
        raise RuntimeError("Weather service not configured (missing WEATHER_API_KEY)")
    return WEATHER_API_KEY

def _call_openweather(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    api_key = _ensure_key()
    parameters = {
        "appid": api_key,
        "units": "imperial",
        **params,
    }
    resp = requests.get(url, params=parameters, timeout=10)
    resp.raise_for_status()
    return resp.json()

@tool
def get_current_weather(city: str) -> str:
    """Get current weather for a given city (temperature, feels-like, description)."""
    try:
        data = _call_openweather(BASE_URL_CURRENT, {"q": city})
    except Exception as e:
        return f"Error fetching current weather for '{city}': {e}"

    try:
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
    except (KeyError, IndexError):
        return f"Couldn't parse weather data for '{city}'."

    return (
        f"In {city}, it's currently {description}, "
        f"{temp:.1f}°F (feels like {feels_like:.1f}°F)."
    )

@tool
def get_forecast(city: str, days: int = 3) -> str:
    """
    Get a simplified multi-day forecast for a city.
    Uses OpenWeather 5-day / 3-hour forecast and summarizes by day.
    """
    if days < 1:
        days = 1
    if days > 5:
        days = 5

    try:
        data = _call_openweather(BASE_URL_FORECAST, {"q": city})
    except Exception as e:
        return f"Error fetching forecast for '{city}': {e}"

    try:
        entries: List[Dict[str, Any]] = data["list"]
    except KeyError:
        return f"Couldn't parse forecast data for '{city}'."

    by_date: Dict[str, List[Dict[str, Any]]] = {}
    for entry in entries:
        dt_txt = entry.get("dt_txt", "")
        date = dt_txt.split(" ")[0]
        by_date.setdefault(date, []).append(entry)

    sorted_dates = sorted(by_date.keys())[:days]
    lines: List[str] = [f"{len(sorted_dates)}-day forecast for {city} (approx):"]

    for d in sorted_dates:
        day_entries = by_date[d]
        temps = [e["main"]["temp"] for e in day_entries if "main" in e]
        descs = [e["weather"][0]["description"] for e in day_entries if "weather" in e]

        if not temps or not descs:
            continue

        avg_temp = sum(temps) / len(temps)
        desc = max(set(descs), key=descs.count)
        lines.append(f"- {d}: around {avg_temp:.1f}°F, mostly {desc}")

    return "\n".join(lines) if len(lines) > 1 else f"No forecast data found for '{city}'."
