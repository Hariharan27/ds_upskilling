from llm_api.llm import LLMClient


def get_llm_client() -> LLMClient:
    """Provide an LLM client to API endpoints."""

    return LLMClient()