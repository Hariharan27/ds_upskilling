from pydantic import BaseModel

from app.domain.models.chat_message import ChatMessage


class ResponseGenerationRequest(BaseModel):

    query: str

    context: str

    conversation_history: list[ChatMessage]


class ResponseGenerationResponse(BaseModel):

    answer: str

    input_tokens: int

    output_tokens: int

    total_tokens: int