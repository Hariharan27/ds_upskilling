from langchain_together import ChatTogether

from app.core.config import get_settings


def get_chat_model() -> ChatTogether:
    """Create the configured Together AI chat model."""

    settings = get_settings()

    return ChatTogether(
        model=settings.together_model,
        together_api_key=settings.together_api_key,
    )