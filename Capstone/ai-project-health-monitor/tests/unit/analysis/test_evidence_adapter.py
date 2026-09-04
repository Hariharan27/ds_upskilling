from datetime import UTC, datetime

from ai_project_health_monitor.analysis.evidence_adapter import EvidenceAdapter
from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult


def test_from_retrieval_results_converts_chunks_to_evidence() -> None:
    occurred_at = datetime(
        2026,
        9,
        1,
        tzinfo=UTC,
    )

    results = [
        RetrievalResult(
            chunk=DocumentChunk(
                chunk_id="CHUNK-001",
                project_id="PROJ-001",
                event_id="EVT-JIRA-001",
                source_type=SourceType.JIRA,
                source_id="EVT-JIRA-001",
                content="Payment API integration is blocked.",
                chunk_index=0,
                occurred_at=occurred_at,
            ),
            score=0.92,
        )
    ]

    evidence = EvidenceAdapter.from_retrieval_results(results)

    assert len(evidence) == 1
    assert evidence[0].source_type == SourceType.JIRA
    assert evidence[0].source_id == "EVT-JIRA-001"
    assert evidence[0].content == "Payment API integration is blocked."
    assert evidence[0].occurred_at == occurred_at


def test_from_retrieval_results_preserves_result_order() -> None:
    occurred_at = datetime(
        2026,
        9,
        1,
        tzinfo=UTC,
    )

    results = [
        RetrievalResult(
            chunk=DocumentChunk(
                chunk_id="CHUNK-001",
                project_id="PROJ-001",
                event_id="EVT-JIRA-001",
                source_type=SourceType.JIRA,
                source_id="EVT-JIRA-001",
                content="Payment integration is blocked.",
                chunk_index=0,
                occurred_at=occurred_at,
            ),
            score=0.92,
        ),
        RetrievalResult(
            chunk=DocumentChunk(
                chunk_id="CHUNK-002",
                project_id="PROJ-001",
                event_id="EVT-EMAIL-001",
                source_type=SourceType.EMAIL,
                source_id="EVT-EMAIL-001",
                content="The release date may be affected.",
                chunk_index=0,
                occurred_at=occurred_at,
            ),
            score=0.85,
        ),
    ]

    evidence = EvidenceAdapter.from_retrieval_results(results)

    assert [item.source_id for item in evidence] == [
        "EVT-JIRA-001",
        "EVT-EMAIL-001",
    ]


def test_from_retrieval_results_returns_empty_for_no_results() -> None:
    evidence = EvidenceAdapter.from_retrieval_results([])

    assert evidence == []