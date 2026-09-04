from datetime import UTC, datetime
from unittest.mock import Mock

import pytest

from ai_project_health_monitor.analysis.health_scorer import HealthScorer
from ai_project_health_monitor.analysis.project_health import ProjectHealthService
from ai_project_health_monitor.analysis.risk_analyzer import RiskAnalyzer
from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.domain.models.health_score import (
    HealthScore,
    HealthStatus,
)
from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.domain.models.risk_signal import (
    RiskSeverity,
    RiskSignal,
    RiskType,
)
from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult


@pytest.fixture
def evidence() -> list[Evidence]:
    return [
        Evidence(
            event_id="EVT-JIRA-001",
            source_type=SourceType.JIRA,
            source_id="EVT-JIRA-001",
            content="Payment API integration is blocked.",
            occurred_at=datetime(
                2026,
                9,
                1,
                tzinfo=UTC,
            ),
        )
    ]


@pytest.fixture
def retrieval_results() -> list[RetrievalResult]:
    return [
        RetrievalResult(
            chunk=DocumentChunk(
                chunk_id="CHUNK-001",
                project_id="PROJ-001",
                event_id="EVT-JIRA-001",
                source_type=SourceType.JIRA,
                source_id="EVT-JIRA-001",
                content="Payment API integration is blocked.",
                chunk_index=0,
                occurred_at=datetime(
                    2026,
                    9,
                    1,
                    tzinfo=UTC,
                ),
            ),
            score=0.92,
        )
    ]


@pytest.fixture
def risk_signal(evidence: list[Evidence]) -> RiskSignal:
    return RiskSignal(
        signal_id="RISK-001",
        project_id="PROJ-001",
        event_id="EVT-JIRA-001",
        risk_type=RiskType.BLOCKER,
        severity=RiskSeverity.HIGH,
        confidence=0.9,
        evidence=evidence[0],
        rationale="Payment integration is blocked.",
    )


@pytest.fixture
def health_score() -> HealthScore:
    return HealthScore(
        project_id="PROJ-001",
        score=82.0,
        status=HealthStatus.HEALTHY,
        contributing_risks=["RISK-001"],
        calculated_at=datetime(
            2026,
            9,
            4,
            tzinfo=UTC,
        ),
        rationale="Project has a manageable blocker risk.",
    )


def test_analyze_coordinates_risk_analysis_and_health_scoring(
    retrieval_results: list[RetrievalResult],
    evidence: list[Evidence],
    risk_signal: RiskSignal,
    health_score: HealthScore,
) -> None:
    risk_analyzer = Mock(spec=RiskAnalyzer)
    health_scorer = Mock(spec=HealthScorer)

    risk_analyzer.analyze.return_value = [risk_signal]
    health_scorer.calculate.return_value = health_score

    service = ProjectHealthService(
        risk_analyzer=risk_analyzer,
        health_scorer=health_scorer,
    )

    result = service.analyze(
        project_id="PROJ-001",
        retrieval_results=retrieval_results,
    )

    assert result == health_score

    risk_analyzer.analyze.assert_called_once_with(
        project_id="PROJ-001",
        evidence=evidence,
    )

    health_scorer.calculate.assert_called_once_with(
        project_id="PROJ-001",
        risk_signals=[risk_signal],
    )


def test_analyze_passes_empty_retrieval_results_to_risk_analyzer(
    health_score: HealthScore,
) -> None:
    risk_analyzer = Mock(spec=RiskAnalyzer)
    health_scorer = Mock(spec=HealthScorer)

    risk_analyzer.analyze.return_value = []
    health_scorer.calculate.return_value = health_score

    service = ProjectHealthService(
        risk_analyzer=risk_analyzer,
        health_scorer=health_scorer,
    )

    result = service.analyze(
        project_id="PROJ-001",
        retrieval_results=[],
    )

    assert result == health_score

    risk_analyzer.analyze.assert_called_once_with(
        project_id="PROJ-001",
        evidence=[],
    )

    health_scorer.calculate.assert_called_once_with(
        project_id="PROJ-001",
        risk_signals=[],
    )


def test_analyze_rejects_empty_project_id(
    retrieval_results: list[RetrievalResult],
) -> None:
    risk_analyzer = Mock(spec=RiskAnalyzer)
    health_scorer = Mock(spec=HealthScorer)

    service = ProjectHealthService(
        risk_analyzer=risk_analyzer,
        health_scorer=health_scorer,
    )

    with pytest.raises(
        ValueError,
        match="project_id cannot be empty",
    ):
        service.analyze(
            project_id="   ",
            retrieval_results=retrieval_results,
        )

    risk_analyzer.analyze.assert_not_called()
    health_scorer.calculate.assert_not_called()