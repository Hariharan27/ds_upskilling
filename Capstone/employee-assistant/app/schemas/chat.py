from pydantic import BaseModel, Field

from app.schemas.rag import RAGSource


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
    )


class ChatResponse(BaseModel):
    answer: str
    sources: list[RAGSource] = Field(default_factory=list)