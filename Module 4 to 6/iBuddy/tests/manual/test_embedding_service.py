from app.infrastructure.embeddings.sentence_transformer_embedding_service import (
    SentenceTransformerEmbeddingService,
)

service = SentenceTransformerEmbeddingService()

embedding = service.embed_text(
    "Employees are eligible for earned leave."
)

print(f"Dimension: {len(embedding)}")

print(
    f"First 5 values: {embedding[:5]}"
)