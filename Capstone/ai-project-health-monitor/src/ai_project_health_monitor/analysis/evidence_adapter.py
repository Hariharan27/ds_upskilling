from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult


class EvidenceAdapter:
    """Convert RAG retrieval results into analysis evidence."""

    @staticmethod
    def from_retrieval_results(
        results: list[RetrievalResult],
    ) -> list[Evidence]:
        """Convert retrieved chunks into evidence objects."""
        return [
            Evidence(
                event_id=result.chunk.event_id,
                source_type=result.chunk.source_type,
                source_id=result.chunk.source_id,
                content=result.chunk.content,
                occurred_at=result.chunk.occurred_at,
            )
            for result in results
        ]