from pydantic import BaseModel, Field

from ai_project_health_monitor.rag.models.chunk import DocumentChunk


class RetrievalResult(BaseModel):
    """A retrieved document chunk with its similarity score."""

    chunk: DocumentChunk
    score: float = Field(ge=0.0, le=1.0)