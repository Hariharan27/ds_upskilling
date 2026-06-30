from functools import lru_cache

from app.application.services.conversational_query_expansion.llm_conversational_query_expansion_service import (
    LlmConversationalQueryExpansionService,
)
from app.domain.services.conversational_query_expansion_service import (
    ConversationalQueryExpansionService,
)
from app.presentation.api.dependencies.llm import (
    get_client,
)


@lru_cache
def get_query_expansion_service() -> ConversationalQueryExpansionService:
    """
    Return a singleton query expansion service.
    """

    return LlmConversationalQueryExpansionService(
        llm_client=get_client(),
    )