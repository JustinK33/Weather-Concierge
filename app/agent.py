# app/agent.py
from langchain.agents import create_agent
from app.tools.weather import get_current_weather, get_forecast
from app.config import settings

SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions about the weather. "
    "Use the tools get_current_weather and get_forecast whenever the user "
    "asks about weather or forecast. "
    "If the question is not about weather, briefly say you only handle weather questions."
)

def build_weather_agent():
    agent = create_agent(
        model=settings.OPENAI_MODEL,
        tools=[get_current_weather, get_forecast],
        system_prompt=SYSTEM_PROMPT,
    )
    return agent

agent = build_weather_agent()
