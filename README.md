# Weather Chat Service API

A FastAPI backend that exposes a weather-focused chat service.  
It uses a LangChain agent with weather tools to answer questions like  
“what’s the weather in New Brunswick today?” or “what’s the forecast for the next 3 days?”

If the user asks about something that isn’t weather, the agent politely says it only handles weather questions.

---

## Tech Stack

- Python 3
- FastAPI
- LangChain
- Pydantic
- OpenAI API
- Docker
- Uvicorn

---

## Features

- Built with `create_agent` from LangChain:
  - Uses `settings.OPENAI_MODEL` as the LLM.
  - Has access to `get_current_weather` and `get_forecast` tools.
- **System prompt behavior:**
  - If the question is about weather or forecast, it calls the tools.
  - If the question is not about weather, it briefly says it only handles weather questions.
  - 
 ---
 
## What I Learned From This Project

Using LangChain agents with tools
I learned how to use create_agent with custom tools (get_current_weather, get_forecast) and a system prompt so the agent automatically decides when to call them.

Building a FastAPI service around an LLM
I saw how to wrap an LLM agent into clean HTTP endpoints (/weather/current, /weather/forecast, /chat) using FastAPI and Pydantic models.

Managing chat sessions and message history
By using ChatSession, ChatMessage, and an in-memory SESSION_STORE, I learned how to keep per-session message history and convert it to LangChain HumanMessage / AIMessage / SystemMessage.

---

## Running the Project

### To run the project locally, follow these steps:

  1. Clone the repo (git clone <url>)
  2. Create a virtual environment (python3 -m venv venv)
  3. Activate the environment (source venv/bin/activate)
  4. Install requirements (pip install -r requirements.txt)
  5. Set or export your OpenAI API key (in .env or export ...)
  6. Run locally (uvicorn app.main:app --reload)
     
### Run with Docker

  2. Build image (docker build -t weather-chat-service -f dockerfile .)
  3. Run image (docker run --rm -p 8000:8000 --env-file .env weather-chat-service) # make sure API key is in .env
