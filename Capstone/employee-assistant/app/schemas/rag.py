from pydantic import BaseModel, Field

class RAGSource(BaseModel):
    """Source document used to answer the question."""

    document: str
    page: int | None = None


class RAGResponse(BaseModel):
    """Structured response from the RAG pipeline."""

    answer: str
    sources: list[RAGSource] = Field(default_factory=list)