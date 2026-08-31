from app.ai.rag.vector_store import get_qdrant_vector_store


def main() -> None:
    query = "Based on the Holiday list can you tell how many holidays are there in 2026?"

    vector_store = get_qdrant_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=10,
    )

    print("=" * 100)
    print("QUERY:")
    print(query)

    for rank, (document, score) in enumerate(results, start=1):
        print("\n" + "-" * 80)
        print("Rank:", rank)
        print("Vector score:", score)
        print("Metadata:", document.metadata)
        print("Content:")
        print(document.page_content)


if __name__ == "__main__":
    main()