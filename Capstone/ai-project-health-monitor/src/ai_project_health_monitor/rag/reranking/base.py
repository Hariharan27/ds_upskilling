from abc import ABC, abstractmethod

from ai_project_health_monitor.rag.models.retrieval import RetrievalResult


class Reranker(ABC):
    """Contract for reranking retrieved document candidates."""

    @abstractmethod
    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        limit: int,
    ) -> list[RetrievalResult]:
        """Rerank candidates for the given query."""
        raise NotImplementedError