from abc import ABC, abstractmethod

from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult


class VectorStore(ABC):
    """Contract for storing and retrieving document chunks."""

    @abstractmethod
    def upsert(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        """Store chunks and their corresponding embeddings."""
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        project_id: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:
        """Retrieve the most relevant chunks for a project."""
        raise NotImplementedError