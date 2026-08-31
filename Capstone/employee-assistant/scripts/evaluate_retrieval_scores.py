from app.ai.rag.vector_store import get_qdrant_vector_store
from tests.evaluation.retrieval_dataset import RETRIEVAL_DATASET


def main() -> None:
    vector_store = get_qdrant_vector_store()

    results = []

    for item in RETRIEVAL_DATASET:
        query = item["query"]
        expected_relevant = item["expected_relevant"]

        retrieved = vector_store.similarity_search_with_score(
            query,
            k=3,
        )

        top_document, top_score = retrieved[0]

        results.append(
            {
                "query": query,
                "expected_relevant": expected_relevant,
                "top_score": top_score,
                "document": top_document.metadata.get(
                    "document_name",
                    "Unknown Document",
                ),
            }
        )

    print("=" * 100)
    print("RETRIEVAL SCORE EVALUATION")
    print("=" * 100)

    for result in results:
        label = (
            "RELEVANT"
            if result["expected_relevant"]
            else "IRRELEVANT"
        )

        print("\n" + "-" * 80)
        print(f"Expected : {label}")
        print(f"Score    : {result['top_score']:.4f}")
        print(f"Document : {result['document']}")
        print(f"Query    : {result['query']}")

    relevant_scores = [
        result["top_score"]
        for result in results
        if result["expected_relevant"]
    ]

    irrelevant_scores = [
        result["top_score"]
        for result in results
        if not result["expected_relevant"]
    ]

    print("\n" + "=" * 100)
    print("SCORE DISTRIBUTION")
    print("=" * 100)

    print("\nRelevant queries:")
    print(f"Count  : {len(relevant_scores)}")
    print(f"Min    : {min(relevant_scores):.4f}")
    print(f"Max    : {max(relevant_scores):.4f}")
    print(f"Average: {sum(relevant_scores) / len(relevant_scores):.4f}")

    print("\nIrrelevant queries:")
    print(f"Count  : {len(irrelevant_scores)}")
    print(f"Min    : {min(irrelevant_scores):.4f}")
    print(f"Max    : {max(irrelevant_scores):.4f}")
    print(
        f"Average: "
        f"{sum(irrelevant_scores) / len(irrelevant_scores):.4f}"
    )


if __name__ == "__main__":
    main()