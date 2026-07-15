import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether
from pydantic import BaseModel,Field,SecretStr

from check_leave_balance import check_leave_balance

load_dotenv()

def tool_call_example():

    api_key = os.getenv("TOGETHER_API_KEY")

    if not api_key:
        raise ValueError(
            "TOGETHER_API_KEY is not configured."
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an HR assistant.

                Use the available tools whenever real employee
                information is required.

                The current employee ID is EMP-101.
                """,
            ),
            (
                "human",
                "{user_input}",
            ),
        ]
    )


    model = ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        temperature=0,
        api_key= SecretStr(api_key)
    )

    tools = [
        check_leave_balance
    ]

    model_with_tools = model.bind_tools(tools)

    chain =  prompt | model_with_tools

    response = chain.invoke(
        {
            "user_input": "How many leaves do I have?",
        }
    )

    print("\n--- MODEL RESPONSE ---")
    print(response)

    print("\n--- CONTENT ---")
    print(response.content)

    print("\n--- TOOL CALLS ---")
    print(response.tool_calls)

    if response.tool_calls:
        tool_call = response.tool_calls[0]

        print(
            "\nRequested tool:",
            tool_call["name"],
        )

        print(
            "Arguments:",
            tool_call["args"],
        )

        if tool_call["name"] == "check_leave_balance":
            tool_result = check_leave_balance.invoke(
                tool_call["args"]
            )

            print(
                "\nTool result:",
                tool_result,
            )



if __name__ == "__main__":
    tool_call_example()

