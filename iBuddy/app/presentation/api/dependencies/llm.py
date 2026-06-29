from functools import lru_cache

from app.domain.services.llm_client import LLMClient
from app.infrastructure.llm.together_llm_client import TogetherLLMClient


@lru_cache
def get_client() -> TogetherLLMClient:
    """
    Return a singleton LLM client.
    """

    return TogetherLLMClient()
