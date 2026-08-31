from app.services.rag_service import answer_policy_question


def main() -> None:
    questions = [
        "How many holidays are there in 2026?",
        "What is the company's stock price today?",
    ]

    for question in questions:
        response = answer_policy_question(question)

        print("\n" + "=" * 100)
        print("QUESTION:")
        print(question)

        print("\nANSWER:")
        print(response.answer)

        print("\nSOURCES:")

        for source in response.sources:
            print(
                f"- {source.document}, "
                f"Page {source.page}"
            )


if __name__ == "__main__":
    main()