from app.domain.models.intent_classification_request import (
    IntentClassificationRequest,
)
from app.domain.models.tool_execution_request import (
    ToolExecutionRequest,
)
from tests.manual.manual_dependencies import (
    get_manual_intent_classifier,
    get_manual_tool_executor,
)


def run_query(
    query: str,
) -> None:

    print()
    print("=" * 100)
    print(f"Query : {query}")
    print("=" * 100)

    classifier = get_manual_intent_classifier()

    classification = classifier.classify(
        IntentClassificationRequest(
            query=query,
            conversation_history=[],
        ),
    )

    print()
    print("Intent Classification")
    print("---------------------")
    print(classification)

    executor = get_manual_tool_executor()

    result = executor.execute(
        classification.tool_name,
        ToolExecutionRequest(
            query=query,
            conversation_history=[],
        ),
    )

    print()
    print("Tool Result")
    print("-----------")
    print(result)

    print("=" * 100)


def main() -> None:

    run_query(
        "What is the WFH policy?",
    )

    run_query(
        "How many earned leaves do I have?",
    )


if __name__ == "__main__":
    main()