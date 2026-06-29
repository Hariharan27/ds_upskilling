from dataclasses import dataclass

from app.domain.models.chat_message import ChatMessage


@dataclass(frozen=True)
class LLMRequest:
    messages: list[ChatMessage]
    temperature: float = 0.0
    max_tokens: int = 512