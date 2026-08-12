import os

from dotenv import load_dotenv
from langchain_together import ChatTogether
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages
from langchain_core.tools import tool

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as exc:
        return f"Calculation error: {exc}"
    

load_dotenv()

llm = ChatTogether(
    model="openai/gpt-oss-20b",
    temperature=0,
)

llm_with_tools = llm.bind_tools([calculator])

response = llm_with_tools.invoke(
    "What is 125 multiplied by 48?"
)

print("Tool calls:")
for tool_call in response.tool_calls:
    print(tool_call)


result = calculator.invoke(tool_call)

print("Tool result:")
print(result)