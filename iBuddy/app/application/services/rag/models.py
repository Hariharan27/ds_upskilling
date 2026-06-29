from pydantic import BaseModel
from pydantic import Field

from app.domain.models.chat_message import ChatMessage


class RAGPromptRequest(BaseModel):
    query: str
    context: str
    conversation_history: list[ChatMessage] = Field(
        default_factory=list,
    )

class RAGResponse(BaseModel):
    answer: str
    sources: list[str]
    input_tokens: int
    output_tokens: int
    total_tokens: int

from pydantic import BaseModel


class RAGRequest(BaseModel):
    query: str
    conversation_history: list[ChatMessage] = Field(
        default_factory=list,
    )