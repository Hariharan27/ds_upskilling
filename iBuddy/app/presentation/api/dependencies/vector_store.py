from functools import lru_cache

from app.domain.repositories.vector_store_repository import VectorStoreRepository
from app.infrastructure.vectorstores.chroma_vector_store_repository import ChromaVectorStoreRepository

@lru_cache
def get_vector_store_repository() -> VectorStoreRepository:
    """
    Return a singleton vector store repository.
    """
    return ChromaVectorStoreRepository()