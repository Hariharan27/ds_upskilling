import os
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

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


tool_node = ToolNode([calculator])

load_dotenv()

llm = ChatTogether(
    model="openai/gpt-oss-20b",
    temperature=0,
)

llm_with_tools = llm.bind_tools([calculator])


response = llm_with_tools.invoke(
    "What is 125 multiplied by 48?"
)

print(response.tool_calls)


def call_model(state: AgentState):
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }

def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "end"
    
    
graph_builder = StateGraph(AgentState)
graph_builder.add_node("llm", call_model)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "llm")

graph_builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        "end": END,
    },
)

graph_builder.add_edge("tools", "llm")

graph = graph_builder.compile()


result = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is 125 multiplied by 48?"
            }
        ]
    }
)

print(result["messages"][-1].content)