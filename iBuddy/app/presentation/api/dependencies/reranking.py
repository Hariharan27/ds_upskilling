from functools import lru_cache

from app.domain.services.reranking_service import (
    RerankingService,
)
from app.infrastructure.reranking.bge_reranking_service import (
    BGERerankingService,
)


@lru_cache
def get_reranking_service() -> RerankingService:
    """
    Return a singleton reranking service.
    """

    return BGERerankingService()