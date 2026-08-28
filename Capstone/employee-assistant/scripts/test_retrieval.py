from app.ai.rag.retrieval import retrieve_documents


def main() -> None:
    queries = [
        "How many WFH days are allowed per month?",
        "How many days of earned leave are credited?",
        "What are the company holidays in 2026?",
        "Who is eligible for work from home?",
    ]

    for query in queries:
        documents = retrieve_documents(query)
        print(f"Query: {query}")

        for rank, document in enumerate(documents, start=1):
            print("\n" + "-" * 80)
            print("Rank:", rank)
            print("Document:", document.metadata.get("document_name"))
            print("Page:", document.metadata.get("page"))
            print("Content:")
            print(document.page_content)

if __name__ == "__main__":
    main()