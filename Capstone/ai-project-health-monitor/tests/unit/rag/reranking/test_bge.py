from unittest.mock import Mock, patch

import pytest

from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.reranking.bge import BGEReranker


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


@patch("ai_project_health_monitor.rag.reranking.bge.CrossEncoder")
def test_bge_reranker_reranks_candidates(
    mock_cross_encoder: Mock,
) -> None:
    mock_model = mock_cross_encoder.return_value
    mock_model.predict.return_value = [0.1, 0.9]

    reranker = BGEReranker()

    results = [
        make_result("EVT-001", 0.8),
        make_result("EVT-002", 0.7),
    ]

    reranked = reranker.rerank(
        query="What is blocked?",
        results=results,
        limit=2,
    )

    assert [result.chunk.event_id for result in reranked] == [
        "EVT-002",
        "EVT-001",
    ]

    assert [result.score for result in reranked] == [
        0.9,
        0.1,
    ]

    mock_model.predict.assert_called_once_with(
        [
            [
                "What is blocked?",
                "Content for EVT-001",
            ],
            [
                "What is blocked?",
                "Content for EVT-002",
            ],
        ],
    )


@patch("ai_project_health_monitor.rag.reranking.bge.CrossEncoder")
def test_bge_reranker_applies_limit(
    mock_cross_encoder: Mock,
) -> None:
    mock_model = mock_cross_encoder.return_value
    mock_model.predict.return_value = [0.1, 0.9, 0.5]

    reranker = BGEReranker()

    results = [
        make_result("EVT-001", 0.8),
        make_result("EVT-002", 0.7),
        make_result("EVT-003", 0.6),
    ]

    reranked = reranker.rerank(
        query="What is blocked?",
        results=results,
        limit=2,
    )

    assert len(reranked) == 2
    assert [result.chunk.event_id for result in reranked] == [
        "EVT-002",
        "EVT-003",
    ]


@patch("ai_project_health_monitor.rag.reranking.bge.CrossEncoder")
def test_bge_reranker_returns_empty_for_empty_results(
    mock_cross_encoder: Mock,
) -> None:
    reranker = BGEReranker()

    result = reranker.rerank(
        query="What is blocked?",
        results=[],
        limit=5,
    )

    assert result == []
    mock_cross_encoder.return_value.predict.assert_not_called()


@pytest.mark.parametrize(
    ("query", "limit"),
    [
        ("", 5),
        ("   ", 5),
        ("What is blocked?", 0),
        ("What is blocked?", -1),
    ],
)
@patch("ai_project_health_monitor.rag.reranking.bge.CrossEncoder")
def test_bge_reranker_rejects_invalid_input(
    mock_cross_encoder: Mock,
    query: str,
    limit: int,
) -> None:
    reranker = BGEReranker()

    with pytest.raises(ValueError):
        reranker.rerank(
            query=query,
            results=[],
            limit=limit,
        )

    mock_cross_encoder.return_value.predict.assert_not_called()