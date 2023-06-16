import json
import logging

from autochain.agent.openai_funtions_agent.openai_functions_agent import (
    OpenAIFunctionAgent,
)
from autochain.chain.chain import Chain
from autochain.memory.buffer_memory import BufferMemory
from autochain.models.chat_openai import ChatOpenAI
from autochain.tools.base import Tool


def get_current_weather(location: str, unit: str = "fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


tools = [
    Tool(
        name="get_current_weather",
        func=get_current_weather,
        description="""Get the current weather in a given location""",
    )
]

memory = BufferMemory()
logging.basicConfig(level=logging.INFO)
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613")
agent = OpenAIFunctionAgent.from_llm_and_tools(llm=llm, tools=tools)
chain = Chain(agent=agent, memory=memory)

# example
user_query = "What's the weather today?"
print(f">> User: {user_query}")
print(f">> Assistant: {chain.run(user_query)['message']}")
next_user_query = "Boston"
print(f">> User: {next_user_query}")
print(f">> Assistant: {chain.run(next_user_query)['message']}")