from sentence_transformers import CrossEncoder

from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.reranking.base import Reranker


class BGEReranker(Reranker):
    """Rerank retrieval candidates using a BGE cross-encoder."""

    MODEL_NAME = "BAAI/bge-reranker-base"

    def __init__(self) -> None:
        self._model = CrossEncoder(
            self.MODEL_NAME,
            activation_fn=None,
        )

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        limit: int,
    ) -> list[RetrievalResult]:
        """Rank candidates by cross-encoder relevance score."""
        if not query.strip():
            raise ValueError("query cannot be empty")

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        if not results:
            return []

        pairs = [
            [query, result.chunk.content]
            for result in results
        ]

        scores = self._model.predict(pairs)

        for result, score in zip(results, scores, strict=True):
            print(
                f"[BGE] "
                f"event_id={result.chunk.event_id} "
                f"score={float(score):.6f} "
                f"content={result.chunk.content[:120]!r}"
            )

        reranked = [
            result.model_copy(update={"score": float(score)})
            for result, score in zip(results, scores, strict=True)
        ]
        
        return sorted(
            reranked,
            key=lambda result: result.score,
            reverse=True,
        )[:limit]