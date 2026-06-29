from functools import lru_cache

from app.application.services.context_builder.default_context_builder import (
    DefaultContextBuilder,
)
from app.application.services.rag.prompt_builder import (
    PromptBuilder,
)
from app.application.services.rag.rag_generation_service import (
    RAGGenerationService,
)
from app.presentation.api.dependencies.llm import (
    get_client,
)
from app.presentation.api.dependencies.multi_query_retrieval import (
    get_multi_query_retrieval_service,
)


@lru_cache
def get_context_builder() -> DefaultContextBuilder:
    """
    Return a singleton context builder.
    """

    return DefaultContextBuilder()


@lru_cache
def get_prompt_builder() -> PromptBuilder:
    """
    Return a singleton prompt builder.
    """

    return PromptBuilder()


@lru_cache
def get_rag_generation_service() -> RAGGenerationService:
    """
    Return a singleton RAG generation service.
    """

    return RAGGenerationService(
        retrieval_service=get_multi_query_retrieval_service(),
        context_builder=get_context_builder(),
        prompt_builder=get_prompt_builder(),
        llm_client=get_client(),
    )