from app.ai.rag.reranking import rerank_documents
from app.ai.rag.vector_store import get_qdrant_vector_store


def main() -> None:
    query = (
        "Based on the Holiday list can you tell "
        "how many holidays are there in 2026?"
    )

    vector_store = get_qdrant_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=10,
    )

    documents = [document for document, _score in results]

    print("=" * 100)
    print("RAW QDRANT RESULTS")

    for rank, (document, score) in enumerate(results, start=1):
        print("\n" + "-" * 80)
        print("Rank:", rank)
        print("Vector score:", score)
        print("Document:", document.metadata.get("document_name"))
        print("Page:", document.metadata.get("page"))

    print("\n" + "=" * 100)
    print("FLASHRANK RESULTS")

    reranked = rerank_documents(
        query=query,
        documents=documents,
        top_n=10,
    )

    for rank, document in enumerate(reranked, start=1):
        print("\n" + "-" * 80)
        print("Rank:", rank)
        print("Reranker score:", document.metadata.get("relevance_score"))
        print("Document:", document.metadata.get("document_name"))
        print("Page:", document.metadata.get("page"))


if __name__ == "__main__":
    main()