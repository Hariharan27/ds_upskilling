from langchain.agents import create_agent
from langchain_together import ChatTogether

from app.config import get_settings
from app.tools import TOOLS


AGENT_SYSTEM_PROMPT = """
You are a travel planning agent.

Your goal is to create a practical travel plan that satisfies
the user's requirements and budget.

Follow these rules strictly:

1. Use the available tools whenever factual information required
   for the plan can be obtained from a tool.

2. Never invent, assume, or guess values that should come from
   a tool.

3. You may call multiple tools together only when their inputs
   are independently known.

4. Do not call a tool using values that are expected to come
   from another tool until those values have been observed.

5. Base subsequent decisions only on:
   - information provided by the user
   - results returned by tools

6. Produce a final answer only when enough verified information
   is available to satisfy the user's request.
"""


def create_llm() -> ChatTogether:
    settings = get_settings()

    return ChatTogether(
        model=settings.together_model,
        api_key=settings.together_api_key,
        temperature=settings.temperature,
    )


def create_travel_agent():
    llm = create_llm()

    return create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt=AGENT_SYSTEM_PROMPT,
    )