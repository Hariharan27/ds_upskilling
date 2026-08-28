from langchain_core.messages import HumanMessage

from app.ai.models.chat import get_chat_model


def main() -> None:
    model = get_chat_model()

    response = model.invoke(
        [
            HumanMessage(
                content="Say hello in one short sentence."
            )
        ]
    )

    print(response.content)


if __name__ == "__main__":
    main()