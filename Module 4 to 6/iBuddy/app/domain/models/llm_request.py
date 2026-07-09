from dataclasses import dataclass

from pydantic import BaseModel

from app.domain.models.chat_message import ChatMessage


@dataclass(frozen=True)
class LLMRequest:
    messages: list[ChatMessage]
    temperature: float = 0.0
    max_tokens: int = 512
    response_schema: type[BaseModel] | None = None