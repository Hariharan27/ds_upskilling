from functools import lru_cache

from app.application.services.query_expansion.llm_query_expansion_service import (
    LlmQueryExpansionService,
)
from app.domain.services.query_expansion_service import (
    QueryExpansionService,
)
from app.presentation.api.dependencies.llm import (
    get_client,
)


@lru_cache
def get_query_expansion_service() -> QueryExpansionService:
    """
    Return a singleton query expansion service.
    """

    return LlmQueryExpansionService(
        llm_client=get_client(),
    )