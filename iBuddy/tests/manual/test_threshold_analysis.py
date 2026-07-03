from app.infrastructure.embeddings.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService,
)

from app.infrastructure.vectorstores.chroma_vector_store_repository import (
    ChromaVectorStoreRepository,
)


QUERIES = [
    "How many WFH days are allowed?",
    "What is the leave policy?",
    "How do I apply for certification reimbursement?",
    "What is the staff loan policy?",
    "What are employee benefits?",
    "What is the whistleblower policy?",
    "What is the code of conduct?",
    "How is access management handled?",
    "What is the incident management process?",
    "What is the asset management policy?",
]


def main() -> None:

    embedding_service = (
        SentenceTransformerEmbeddingService()
    )

    vector_store = (
        ChromaVectorStoreRepository()
    )

    for query in QUERIES:

        print("\n" + "=" * 100)
        print(f"QUERY: {query}")
        print("=" * 100)

        query_embedding = (
            embedding_service.embed_text(query)
        )

        response = (
            vector_store._collection.query(
                query_embeddings=[query_embedding],
                n_results=5,
            )
        )

        distances = response["distances"][0]
        metadatas = response["metadatas"][0]

        for rank, (
            distance,
            metadata,
        ) in enumerate(
            zip(
                distances,
                metadatas,
            ),
            start=1,
        ):
            similarity = (
                1 - distance
            )

            print(
                f"Rank={rank} | "
                f"Similarity={similarity:.3f} | "
                f"File={metadata.get('file_name')}"
            )


if __name__ == "__main__":
    main()