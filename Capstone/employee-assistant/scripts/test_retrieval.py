from app.ai.rag.retrieval import retrieve_documents


def main() -> None:
    queries = [
        "How many holidays are there in 2026?",
        "How many WFH days are allowed per month?",
        "What is the company's stock price today?",
        "What is the weather today?",
    ]

    for query in queries:
        documents = retrieve_documents(
            query=query,
            k=3,
        )

        print("\n" + "=" * 100)
        print("QUERY:", query)
        print("RETRIEVED DOCUMENTS:", len(documents))

        for rank, document in enumerate(documents, start=1):
            print("\n" + "-" * 80)
            print("Rank:", rank)
            print(
                "Document:",
                document.metadata.get(
                    "document_name",
                    "Unknown Document",
                ),
            )
            print("Page:", document.metadata.get("page"))


if __name__ == "__main__":
    main()