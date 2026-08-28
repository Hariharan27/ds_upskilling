from app.ai.rag.context import build_context
from app.ai.rag.retrieval import retrieve_documents


def main() -> None:
    question = "Based on the Holiday list can you tell how many holidays are there in 2026?"

    documents = retrieve_documents(
        query=question,
        k=10,
        top_n=3,
    )

    print("=" * 100)
    print("QUESTION:")
    print(question)

    print("\n" + "=" * 100)
    print("RETRIEVED CONTEXT")

    for rank, document in enumerate(documents, start=1):
        print("\n" + "-" * 80)
        print("Rank:", rank)
        print("Document:", document.metadata.get("document_name"))
        print("Page:", document.metadata.get("page"))
        print("Score:", document.metadata.get("relevance_score"))
        print(document.page_content)

    print("\n" + "=" * 100)
    print("FORMATTED CONTEXT")

    print(build_context(documents))


if __name__ == "__main__":
    main()