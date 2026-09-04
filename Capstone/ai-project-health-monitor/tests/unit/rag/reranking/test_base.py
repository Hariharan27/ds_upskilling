import pytest

from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.reranking.base import Reranker


def make_result(
    event_id: str,
    score: float,
) -> RetrievalResult:
    return RetrievalResult(
        chunk=DocumentChunk(
            chunk_id=f"{event_id}-CHUNK-000",
            project_id="PROJ-001",
            event_id=event_id,
            source_type="jira",
            source_id=event_id,
            content=f"Content for {event_id}",
            chunk_index=0,
            occurred_at="2026-09-01T10:00:00Z",
        ),
        score=score,
    )


class FakeReranker(Reranker):
    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        limit: int,
    ) -> list[RetrievalResult]:
        return sorted(
            results,
            key=lambda result: result.score,
            reverse=True,
        )[:limit]


def test_reranker_can_be_implemented() -> None:
    reranker = FakeReranker()

    results = [
        make_result("EVT-001", 0.60),
        make_result("EVT-002", 0.90),
    ]

    reranked = reranker.rerank(
        query="What is blocked?",
        results=results,
        limit=1,
    )

    assert len(reranked) == 1
    assert reranked[0].chunk.event_id == "EVT-002"


def test_reranker_is_abstract() -> None:
    with pytest.raises(TypeError):
        Reranker()