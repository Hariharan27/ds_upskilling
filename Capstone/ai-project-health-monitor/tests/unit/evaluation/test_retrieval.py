from datetime import UTC, datetime

import pytest

from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.evaluation.models.retrieval import (
    RetrievalEvaluationCase,
)
from ai_project_health_monitor.evaluation.retrieval import RetrievalEvaluator
from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult


def make_result(
    event_id: str,
    project_id: str,
    score: float = 0.9,
) -> RetrievalResult:
    """Create a deterministic retrieval result for testing."""
    chunk = DocumentChunk(
        chunk_id=f"{event_id}-CHUNK-000",
        project_id=project_id,
        event_id=event_id,
        source_type=SourceType.JIRA,
        source_id=event_id,
        content=f"Evidence for {event_id}",
        chunk_index=0,
        occurred_at=datetime(
            2026,
            9,
            1,
            tzinfo=UTC,
        ),
    )

    return RetrievalResult(
        chunk=chunk,
        score=score,
    )


@pytest.fixture
def evaluation_case() -> RetrievalEvaluationCase:
    return RetrievalEvaluationCase(
        query_id="RAG-001",
        query="Why is the payment integration blocked?",
        project_id="PROJ-001",
        relevant_event_ids=["EVT-001"],
    )


def test_evaluate_case_calculates_hit_precision_and_recall(
    evaluation_case: RetrievalEvaluationCase,
) -> None:
    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        assert query == evaluation_case.query
        assert project_id == evaluation_case.project_id
        assert limit == 3

        return [
            make_result("EVT-001", "PROJ-001"),
            make_result("EVT-002", "PROJ-001"),
            make_result("EVT-003", "PROJ-001"),
        ]

    evaluator = RetrievalEvaluator(retrieve)

    result = evaluator.evaluate_case(evaluation_case, k=3)

    assert result.query_id == "RAG-001"
    assert result.retrieved_event_ids == [
        "EVT-001",
        "EVT-002",
        "EVT-003",
    ]
    assert result.hit is True
    assert result.precision_at_k == pytest.approx(1 / 3)
    assert result.recall_at_k == 1.0
    assert result.cross_project_results == []


def test_evaluate_case_detects_missed_relevant_event(
    evaluation_case: RetrievalEvaluationCase,
) -> None:
    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        return [
            make_result("EVT-002", "PROJ-001"),
            make_result("EVT-003", "PROJ-001"),
        ]

    evaluator = RetrievalEvaluator(retrieve)

    result = evaluator.evaluate_case(evaluation_case, k=2)

    assert result.hit is False
    assert result.precision_at_k == 0.0
    assert result.recall_at_k == 0.0


def test_evaluate_case_handles_multiple_relevant_events() -> None:
    case = RetrievalEvaluationCase(
        query_id="RAG-002",
        query="Is the release date at risk?",
        project_id="PROJ-001",
        relevant_event_ids=[
            "EVT-001",
            "EVT-002",
        ],
    )

    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        return [
            make_result("EVT-001", "PROJ-001"),
            make_result("EVT-003", "PROJ-001"),
            make_result("EVT-002", "PROJ-001"),
        ]

    evaluator = RetrievalEvaluator(retrieve)

    result = evaluator.evaluate_case(case, k=3)

    assert result.hit is True
    assert result.precision_at_k == pytest.approx(2 / 3)
    assert result.recall_at_k == 1.0


def test_evaluate_case_detects_cross_project_results(
    evaluation_case: RetrievalEvaluationCase,
) -> None:
    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        return [
            make_result("EVT-001", "PROJ-001"),
            make_result("EVT-201", "PROJ-002"),
        ]

    evaluator = RetrievalEvaluator(retrieve)

    result = evaluator.evaluate_case(evaluation_case, k=2)

    assert result.hit is True
    assert result.cross_project_results == ["EVT-201"]


def test_evaluate_case_handles_empty_retrieval_results(
    evaluation_case: RetrievalEvaluationCase,
) -> None:
    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        return []

    evaluator = RetrievalEvaluator(retrieve)

    result = evaluator.evaluate_case(evaluation_case, k=5)

    assert result.hit is False
    assert result.precision_at_k == 0.0
    assert result.recall_at_k == 0.0
    assert result.cross_project_results == []


def test_evaluate_aggregates_results() -> None:
    cases = [
        RetrievalEvaluationCase(
            query_id="RAG-001",
            query="Query one",
            project_id="PROJ-001",
            relevant_event_ids=["EVT-001"],
        ),
        RetrievalEvaluationCase(
            query_id="RAG-002",
            query="Query two",
            project_id="PROJ-001",
            relevant_event_ids=["EVT-002"],
        ),
    ]

    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        if query == "Query one":
            return [
                make_result("EVT-001", "PROJ-001"),
                make_result("EVT-003", "PROJ-001"),
            ]

        return [
            make_result("EVT-004", "PROJ-001"),
        ]

    evaluator = RetrievalEvaluator(retrieve)

    summary = evaluator.evaluate(cases, k=2)

    assert summary.total_cases == 2
    assert summary.hit_rate == 0.5
    assert summary.mean_precision_at_k == pytest.approx(0.25)
    assert summary.mean_recall_at_k == 0.5
    assert summary.cross_project_result_count == 0


def test_evaluate_hit_rate_uses_positive_cases_only() -> None:
    cases = [
        RetrievalEvaluationCase(
            query_id="RAG-001",
            query="What is blocked?",
            project_id="PROJ-001",
            relevant_event_ids=["EVT-001"],
        ),
        RetrievalEvaluationCase(
            query_id="RAG-NEG-001",
            query="What database migration was completed?",
            project_id="PROJ-001",
            relevant_event_ids=[],
        ),
    ]

    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        if query == "What is blocked?":
            return [
                make_result("EVT-001", "PROJ-001"),
            ]

        return [
            make_result("EVT-002", "PROJ-001"),
        ]

    evaluator = RetrievalEvaluator(retrieve)

    summary = evaluator.evaluate(cases, k=3)

    assert summary.total_cases == 2
    assert summary.hit_rate == 1.0

def test_evaluate_empty_dataset() -> None:
    evaluator = RetrievalEvaluator(
        lambda query, project_id, limit: [],
    )

    summary = evaluator.evaluate([], k=5)

    assert summary.total_cases == 0
    assert summary.hit_rate == 0.0
    assert summary.mean_precision_at_k == 0.0
    assert summary.mean_recall_at_k is None
    assert summary.cross_project_result_count == 0


@pytest.mark.parametrize("k", [0, -1])
def test_evaluate_case_rejects_invalid_k(
    evaluation_case: RetrievalEvaluationCase,
    k: int,
) -> None:
    evaluator = RetrievalEvaluator(
        lambda query, project_id, limit: [],
    )

    with pytest.raises(
        ValueError,
        match="k must be greater than zero",
    ):
        evaluator.evaluate_case(evaluation_case, k)


@pytest.mark.parametrize("k", [0, -1])
def test_evaluate_rejects_invalid_k(k: int) -> None:
    evaluator = RetrievalEvaluator(
        lambda query, project_id, limit: [],
    )

    with pytest.raises(
        ValueError,
        match="k must be greater than zero",
    ):
        evaluator.evaluate([], k)

def test_evaluate_case_handles_negative_query_without_results() -> None:
    case = RetrievalEvaluationCase(
        query_id="RAG-NEG-001",
        query="What database migration was completed?",
        project_id="PROJ-001",
        relevant_event_ids=[],
    )

    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        return []

    evaluator = RetrievalEvaluator(retrieve)

    result = evaluator.evaluate_case(case, k=3)

    assert result.hit is True
    assert result.precision_at_k == 0.0
    assert result.recall_at_k is None
    assert result.false_positive_count == 0

def test_evaluate_case_detects_negative_query_false_positives() -> None:
    case = RetrievalEvaluationCase(
        query_id="RAG-NEG-002",
        query="What database migration was completed?",
        project_id="PROJ-001",
        relevant_event_ids=[],
    )

    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        return [
            make_result("EVT-001", "PROJ-001"),
            make_result("EVT-002", "PROJ-001"),
        ]

    evaluator = RetrievalEvaluator(retrieve)

    result = evaluator.evaluate_case(case, k=3)

    assert result.hit is False
    assert result.recall_at_k is None
    assert result.false_positive_count == 2

def test_evaluate_aggregates_negative_cases() -> None:
    cases = [
        RetrievalEvaluationCase(
            query_id="RAG-001",
            query="Positive query",
            project_id="PROJ-001",
            relevant_event_ids=["EVT-001"],
        ),
        RetrievalEvaluationCase(
            query_id="RAG-NEG-001",
            query="Negative query",
            project_id="PROJ-001",
            relevant_event_ids=[],
        ),
    ]

    def retrieve(
        query: str,
        project_id: str,
        limit: int,
    ) -> list[RetrievalResult]:
        if query == "Positive query":
            return [make_result("EVT-001", "PROJ-001")]

        return [make_result("EVT-002", "PROJ-001")]

    evaluator = RetrievalEvaluator(retrieve)

    summary = evaluator.evaluate(cases, k=3)

    assert summary.total_cases == 2
    assert summary.negative_cases == 1
    assert summary.negative_false_positive_cases == 1
    assert summary.mean_recall_at_k == 1.0