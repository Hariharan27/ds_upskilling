from app.agent import create_llm
from app.tools import TOOLS

llm = create_llm()

llm_with_tools = llm.bind_tools(TOOLS)

response = llm_with_tools.invoke(
    "Plan a trip from Chennai to Goa for two people."
)

print(response)