from langchain_core.messages import HumanMessage

from app.agent import create_travel_agent


agent = create_travel_agent()

result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Plan a trip from Chennai to Goa "
                    "for two people for two days within a budget of ₹30,000."
                )
            )
        ]
    }
)

print("\n" + "=" * 80)
print("COMPLETE AGENT STATE")
print("=" * 80)

for index, message in enumerate(
    result["messages"],
    start=1,
):
    print(
        f"\nMESSAGE {index}: "
        f"{type(message).__name__}"
    )

    print("Content:")
    print(message.content)

    if hasattr(message, "tool_calls"):
        if message.tool_calls:
            print("Tool Calls:")
            print(message.tool_calls)