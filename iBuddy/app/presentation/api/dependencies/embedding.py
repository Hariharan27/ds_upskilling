from functools import lru_cache

from app.domain.services.embedding_service import  EmbeddingService
from app.infrastructure.embeddings.sentence_transformer_embedding_service import SentenceTransformerEmbeddingService

@lru_cache
def get_embedding_service() -> EmbeddingService:
    """
    Return a singleton embedding service.
    """
    return SentenceTransformerEmbeddingService()