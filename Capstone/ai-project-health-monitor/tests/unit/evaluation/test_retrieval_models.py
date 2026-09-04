import pytest
from pydantic import ValidationError

from ai_project_health_monitor.evaluation.models.retrieval import (
    RetrievalEvaluationCase,
    RetrievalEvaluationResult,
    RetrievalEvaluationSummary,
)


def test_retrieval_evaluation_case_accepts_valid_data() -> None:
    case = RetrievalEvaluationCase(
        query_id="RAG-001",
        query="Why is the payment integration blocked?",
        project_id="PROJ-001",
        relevant_event_ids=["EVT-JIRA-001"],
    )

    assert case.query_id == "RAG-001"
    assert case.project_id == "PROJ-001"
    assert case.relevant_event_ids == ["EVT-JIRA-001"]


@pytest.mark.parametrize(
    "field",
    [
        "query_id",
        "query",
        "project_id",
    ],
)
def test_retrieval_evaluation_case_rejects_empty_required_fields(
    field: str,
) -> None:
    data = {
        "query_id": "RAG-001",
        "query": "Test query",
        "project_id": "PROJ-001",
        "relevant_event_ids": ["EVT-001"],
    }

    data[field] = ""

    with pytest.raises(ValidationError):
        RetrievalEvaluationCase(**data)


def test_retrieval_evaluation_case_allows_no_relevant_events() -> None:
    case = RetrievalEvaluationCase(
        query_id="RAG-NEG-001",
        query="What database migration was completed?",
        project_id="PROJ-001",
        relevant_event_ids=[],
    )

    assert case.relevant_event_ids == []


def test_retrieval_evaluation_result_accepts_valid_data() -> None:
    result = RetrievalEvaluationResult(
    query_id="RAG-001",
    retrieved_event_ids=["EVT-001", "EVT-002"],
    relevant_event_ids=["EVT-001"],
    hit=True,
    precision_at_k=0.5,
    recall_at_k=1.0,
    false_positive_count=1,
    cross_project_results=[],
    )

    assert result.hit is True
    assert result.precision_at_k == 0.5
    assert result.recall_at_k == 1.0
    assert result.cross_project_results == []


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("precision_at_k", -0.1),
        ("precision_at_k", 1.1),
        ("recall_at_k", -0.1),
        ("recall_at_k", 1.1),
    ],
)
def test_retrieval_evaluation_result_rejects_invalid_metrics(
    field: str,
    value: float,
) -> None:
    data = {
        "query_id": "RAG-001",
        "retrieved_event_ids": ["EVT-001"],
        "relevant_event_ids": ["EVT-001"],
        "hit": True,
        "precision_at_k": 1.0,
        "recall_at_k": 1.0,
    }

    data[field] = value

    with pytest.raises(ValidationError):
        RetrievalEvaluationResult(**data)


def test_retrieval_evaluation_summary_accepts_valid_data() -> None:
    summary = RetrievalEvaluationSummary(
        total_cases=4,
        hit_rate=0.75,
        mean_precision_at_k=0.5,
        mean_recall_at_k=0.75,
        cross_project_result_count=0,
        negative_cases=0,
        negative_false_positive_cases=0,
    )

    assert summary.total_cases == 4
    assert summary.hit_rate == 0.75
    assert summary.mean_precision_at_k == 0.5
    assert summary.mean_recall_at_k == 0.75


@pytest.mark.parametrize(
    "field",
    [
        "hit_rate",
        "mean_precision_at_k",
        "mean_recall_at_k",
    ],
)
def test_retrieval_evaluation_summary_rejects_invalid_metrics(
    field: str,
) -> None:
    data = {
        "total_cases": 1,
        "hit_rate": 1.0,
        "mean_precision_at_k": 1.0,
        "mean_recall_at_k": 1.0,
        "cross_project_result_count": 0,
    }

    data[field] = 1.1

    with pytest.raises(ValidationError):
        RetrievalEvaluationSummary(**data)