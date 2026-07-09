from pydantic import BaseModel
from pydantic import Field

from app.domain.models.chat_message import ChatMessage


class ChatRequest(BaseModel):
    query: str
    conversation_history: list[ChatMessage] = Field(
        default_factory=list,
    )


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

    input_tokens: int
    output_tokens: int
    total_tokens: int