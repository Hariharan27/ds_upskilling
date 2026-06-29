from functools import lru_cache

from app.application.services.retrieval.retrieval_service import (
    RetrievalService,
)
from app.presentation.api.dependencies.embedding import (
    get_embedding_service,
)
from app.presentation.api.dependencies.vector_store import (
    get_vector_store_repository,
)

@lru_cache
def get_retrieval_service() -> RetrievalService:
    """
    Return a singleton retrieval service.
    """

    return RetrievalService(
        embedding_service=get_embedding_service(),
        vector_repository=get_vector_store_repository(),
    )

