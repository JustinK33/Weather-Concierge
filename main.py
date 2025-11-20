from langchain.agents import create_agent
from weather import get_weather

agent = create_agent(
    model="gpt-oss-120b",
    tools=[get_weather],
    system_prompt=("You are a helpful assistant that answers questions about the weather. "
                    "Use the get_weather tool whenever the user asks about weather."
    )
)

if __name__=="__main__":
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
    )
    print(response)