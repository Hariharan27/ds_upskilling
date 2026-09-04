from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.reranking.base import Reranker


class RerankingService:
    """Application service responsible for reranking retrieval candidates."""

    def __init__(self, reranker: Reranker) -> None:
        self._reranker = reranker

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        limit: int = 5,
    ) -> list[RetrievalResult]:
        """Rerank retrieval candidates for a query."""
        if not query.strip():
            raise ValueError("query cannot be empty")

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        if not results:
            return []

        return self._reranker.rerank(
            query=query,
            results=results,
            limit=limit,
        )