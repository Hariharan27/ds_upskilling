import pytest

from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.reranking.base import Reranker
from ai_project_health_monitor.rag.reranking.service import RerankingService


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
        return results[:limit]


def test_reranking_service_delegates_to_reranker() -> None:
    reranker = FakeReranker()
    service = RerankingService(reranker)

    results = [
        make_result("EVT-001", 0.9),
        make_result("EVT-002", 0.8),
    ]

    reranked = service.rerank(
        query="What is blocked?",
        results=results,
        limit=1,
    )

    assert len(reranked) == 1
    assert reranked[0].chunk.event_id == "EVT-001"


def test_reranking_service_returns_empty_for_empty_results() -> None:
    service = RerankingService(FakeReranker())

    result = service.rerank(
        query="What is blocked?",
        results=[],
        limit=5,
    )

    assert result == []


@pytest.mark.parametrize(
    ("query", "limit"),
    [
        ("", 5),
        ("   ", 5),
        ("What is blocked?", 0),
        ("What is blocked?", -1),
    ],
)
def test_reranking_service_rejects_invalid_input(
    query: str,
    limit: int,
) -> None:
    service = RerankingService(FakeReranker())

    with pytest.raises(ValueError):
        service.rerank(
            query=query,
            results=[],
            limit=limit,
        )