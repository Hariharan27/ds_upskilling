from langchain_core.messages import HumanMessage

from app.agent import create_travel_agent


agent = create_travel_agent()

for chunk in agent.stream(
    {
        "messages": [
            HumanMessage(
                content=(
                    "Plan a trip from Chennai to Goa "
                    "for two people for two days "
                    "within a budget of ₹30,000."
                )
            )
        ]
    },
    stream_mode="updates",
):
    print("\n" + "=" * 80)
    print("AGENT UPDATE")
    print("=" * 80)
    print(chunk)