import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether
from pydantic import SecretStr


load_dotenv()

def main() -> None:

    user_input = "I want to take leave tomorrow."

    input = {
        "user_input": user_input,
    }

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                 """
                You are an intent classifier for an HR assistant.

                Classify the employee request into exactly one
                of the following intents:

                - apply_leave
                - check_leave_balance
                - search_policy

                Return only the intent name.
                """,
            ),
            (
            "human",
            "{user_input}",
            ),
        ]
    )

    prompt_output = prompt.invoke(input)

    print("==="*80)
    print(prompt_output)
    print(f"Type: {type(prompt_output)}")
    print("==="*80)

    api_key = os.getenv("TOGETHER_API_KEY")

    if not api_key:
        raise ValueError(
            "TOGETHER_API_KEY is not set. Check your .env file."
        )

    model = ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        temperature=0,
        api_key=SecretStr(api_key),
    )

    model_output = model.invoke(prompt_output)
    print("==="*80)
    print(model_output)
    print(f"Type: {type(model_output)}")
    print("==="*80)

    parser = StrOutputParser()

    parser_output = parser.invoke(model_output)
    print("==="*80)
    print(parser_output)
    print(f"Type: {type(parser_output)}")
    print("==="*80)

    chain = prompt | model | parser

    result = chain.invoke(input)

    print("User:", user_input)
    print("Intent:", result)

if __name__ == "__main__":
    main()