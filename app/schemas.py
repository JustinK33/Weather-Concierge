# app/schemas.py
from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from typing import Optional, Annotated

class TemperatureUnit(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class SpeedUnit(str, Enum):
    mph = "mph"
    kph = "kph"


class ChatMessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class Location(BaseModel):
    city: Annotated[str, Field(..., examples=["New Brunswick"])]
    state: Annotated[Optional[str], Field(default=None, examples=["NJ"])]
    country_code: Annotated[str, Field(default="US", examples=["US"])]
    lat: Annotated[Optional[float], Field(default=None, description="Latitude if known")]
    lon: Annotated[Optional[float], Field(default=None, description="Longitude if known")]

class UserPreferences(BaseModel):
    temperature_unit: TemperatureUnit = TemperatureUnit.fahrenheit
    speed_unit: SpeedUnit = SpeedUnit.mph
    default_location: Optional[Location] = None

class WeatherSummary(BaseModel):
    description: Annotated[str, Field(..., examples=["light rain"])]
    temperature: Annotated[float, Field(..., examples=[72.5])]
    feels_like: Annotated[float, Field(..., examples=[70.0])]
    humidity: Annotated[Optional[int], Field(default=None, examples=[60], description="Percent humidity")]
    wind_speed: Annotated[Optional[float], Field(default=None, examples=[5.2])]
    temperature_unit: TemperatureUnit = TemperatureUnit.fahrenheit
    speed_unit: SpeedUnit = SpeedUnit.mph

class ForecastDay(BaseModel):
    date: datetime
    summary: WeatherSummary

class ChatMessage(BaseModel):
    role: ChatMessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage] = []
    preferences: UserPreferences = Field(default_factory=UserPreferences)

class BaseWeatherQuery(BaseModel):
    location: Location
    temperature_unit: TemperatureUnit = TemperatureUnit.fahrenheit

class CurrentWeatherRequest(BaseWeatherQuery):
    pass

class ForecastRequest(BaseWeatherQuery):
    days: int = Field(3, ge=1, le=5)

class CurrentWeatherResponse(BaseModel):
    location: Location
    summary: WeatherSummary
    raw_source: Optional[dict] = Field(
        None, description="Optional raw JSON from provider (for debugging)"
    )

class ForecastResponse(BaseModel):
    location: Location
    days: List[ForecastDay]
    raw_source: Optional[dict] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    location_override: Optional[Location] = None
    preferences_override: Optional[UserPreferences] = None

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    session: ChatSession
    detected_location: Optional[Location] = None
