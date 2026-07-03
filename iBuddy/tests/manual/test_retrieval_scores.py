from app.infrastructure.embeddings.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService,
)

from app.infrastructure.vectorstores.chroma_vector_store_repository import (
    ChromaVectorStoreRepository,
)


def main() -> None:

    query = "How many WFH days are allowed?"

    embedding_service = (
        SentenceTransformerEmbeddingService()
    )

    vector_store = (
        ChromaVectorStoreRepository()
    )

    query_embedding = (
        embedding_service.embed_text(query)
    )

    response = (
        vector_store._collection.query(
            query_embeddings=[query_embedding],
            n_results=10,
        )
    )

    ids = response["ids"][0]
    documents = response["documents"][0]
    metadatas = response["metadatas"][0]
    distances = response["distances"][0]

    print("\n=== QUERY ===")
    print(query)

    print("\n=== RESULTS ===")

    for rank, (
        chunk_id,
        document,
        metadata,
        distance,
    ) in enumerate(
        zip(
            ids,
            documents,
            metadatas,
            distances,
        ),
        start=1,
    ):
        print(f"\nRank: {rank}")
        print(f"Distance: {distance}")
        print(f"File: {metadata.get('file_name')}")
        print(f"Department: {metadata.get('department')}")
        print(f"Category: {metadata.get('category')}")
        print(f"Chunk Id: {chunk_id}")
        print(f"Preview: {document[:250]}")
        print(
            f"Similarity: {1 - distance}"
        )

        print("-" * 80)


if __name__ == "__main__":
    main()