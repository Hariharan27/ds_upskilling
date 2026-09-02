from functools import lru_cache

from langchain_together import ChatTogether

from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_chat_model() -> ChatTogether:
    """Create and cache the configured Together AI chat model."""

    settings = get_settings()

    return ChatTogether(
        model=settings.together_model,
        together_api_key=settings.together_api_key,
    )