from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Message sent to the LLM.",
    )
    conversation_id: str | None = Field(
        default=None,
        description="Optional conversation identifier.",
    )


class ChatResponse(BaseModel):
    """Response returned by the chat endpoint."""

    response: str
    conversation_id: str


class HealthResponse(BaseModel):
    """Response returned by the health endpoint."""

    status: str