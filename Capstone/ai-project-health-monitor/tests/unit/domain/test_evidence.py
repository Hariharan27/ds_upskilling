from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.domain.models.project_event import SourceType


def test_evidence_creation() -> None:
    occurred_at = datetime(2026, 9, 3, 10, 30, tzinfo=UTC)

    evidence = Evidence(
        event_id="EVT-JIRA-001",
        source_type=SourceType.JIRA,
        source_id="JIRA-101",
        content="Payment API integration is blocked.",
        occurred_at=occurred_at,
    )

    assert evidence.source_type == SourceType.JIRA
    assert evidence.source_id == "JIRA-101"
    assert evidence.content == "Payment API integration is blocked."
    assert evidence.occurred_at == occurred_at


@pytest.mark.parametrize(
    "field",
    ["source_type", "source_id", "content"],
)
def test_evidence_rejects_empty_required_fields(field: str) -> None:
    data = {
        "source_type": SourceType.JIRA,
        "source_id": "JIRA-101",
        "content": "Payment API integration is blocked.",
        "occurred_at": datetime.now(UTC),
    }

    if field == "source_type":
        data[field] = None
    else:
        data[field] = ""

    with pytest.raises(ValidationError):
        Evidence(**data)