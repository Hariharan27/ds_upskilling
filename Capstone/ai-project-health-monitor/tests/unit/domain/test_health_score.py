from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from ai_project_health_monitor.domain.models.health_score import (
    HealthScore,
    HealthStatus,
)


def test_health_score_creation() -> None:
    calculated_at = datetime(2026, 9, 3, 10, 30, tzinfo=UTC)

    health = HealthScore(
        project_id="PROJ-001",
        score=62.0,
        status=HealthStatus.AT_RISK,
        contributing_risks=["RISK-001", "RISK-002"],
        calculated_at=calculated_at,
        rationale="Multiple high-severity risks are affecting delivery.",
    )

    assert health.score == 62.0
    assert health.status == HealthStatus.AT_RISK
    assert health.contributing_risks == ["RISK-001", "RISK-002"]


@pytest.mark.parametrize("score", [-1.0, 100.1])
def test_score_must_be_between_zero_and_one_hundred(
    score: float,
) -> None:
    with pytest.raises(ValidationError):
        HealthScore(
            project_id="PROJ-001",
            score=score,
            status=HealthStatus.HEALTHY,
            calculated_at=datetime.now(UTC),
            rationale="Project is progressing as planned.",
        )


def test_contributing_risks_defaults_to_empty_list() -> None:
    health = HealthScore(
        project_id="PROJ-001",
        score=90.0,
        status=HealthStatus.HEALTHY,
        calculated_at=datetime.now(UTC),
        rationale="No significant risks detected.",
    )

    assert health.contributing_risks == []


def test_health_score_rejects_empty_project_id() -> None:
    with pytest.raises(ValidationError):
        HealthScore(
            project_id="",
            score=80.0,
            status=HealthStatus.HEALTHY,
            calculated_at=datetime.now(UTC),
            rationale="Project is healthy.",
        )