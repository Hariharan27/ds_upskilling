from functools import lru_cache

from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_langfuse() -> Langfuse:
    """Create and cache the Langfuse client."""

    settings = get_settings()

    return Langfuse(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        base_url=settings.langfuse_base_url,
    )


@lru_cache(maxsize=1)
def get_langfuse_handler() -> CallbackHandler:
    """Create and cache the Langfuse LangChain callback handler."""

    settings = get_settings()

    return CallbackHandler(
        public_key=settings.langfuse_public_key,
    )