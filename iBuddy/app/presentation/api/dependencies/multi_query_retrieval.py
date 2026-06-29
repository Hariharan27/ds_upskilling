from functools import lru_cache

from app.application.services.retrieval.multi_query_retrieval_service import (
    MultiQueryRetrievalService,
)
from app.presentation.api.dependencies.query_expansion import (
    get_query_expansion_service,
)
from app.presentation.api.dependencies.retrieval import (
    get_retrieval_service,
)
from app.presentation.api.dependencies.reranking import (
    get_reranking_service,
)


@lru_cache
def get_multi_query_retrieval_service() -> MultiQueryRetrievalService:
    """
    Return a singleton multi-query retrieval service.
    """

    return MultiQueryRetrievalService(
        query_expand_service=get_query_expansion_service(),
        retrival_service=get_retrieval_service(),
        reranking_service=get_reranking_service(),
    )