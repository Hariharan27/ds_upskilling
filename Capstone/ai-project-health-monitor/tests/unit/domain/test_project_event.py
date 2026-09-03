from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from ai_project_health_monitor.domain.models.project_event import (
    ProjectEvent,
    SourceType,
)


def test_project_event_creation() -> None:
    occurred_at = datetime(2026, 9, 3, 10, 30, tzinfo=UTC)

    event = ProjectEvent(
        event_id="EVT-001",
        project_id="PROJ-001",
        source_type="jira",
        source_id="JIRA-101",
        content="Backend integration is blocked by API dependency.",
        author="developer@example.com",
        occurred_at=occurred_at,
    )

    assert event.source_type == SourceType.JIRA
    assert event.project_id == "PROJ-001"
    assert event.occurred_at == occurred_at


def test_project_event_metadata_defaults_to_empty_dict() -> None:
    event = ProjectEvent(
        event_id="EVT-001",
        project_id="PROJ-001",
        source_type=SourceType.EMAIL,
        source_id="EMAIL-001",
        content="Client requested additional scope.",
        occurred_at=datetime.now(UTC),
    )

    assert event.metadata == {}


@pytest.mark.parametrize(
    "field",
    ["event_id", "project_id", "source_id", "content"],
)
def test_project_event_rejects_empty_required_fields(field: str) -> None:
    data = {
        "event_id": "EVT-001",
        "project_id": "PROJ-001",
        "source_type": "document",
        "source_id": "DOC-001",
        "content": "Project status update.",
        "occurred_at": datetime.now(UTC),
    }

    data[field] = ""

    with pytest.raises(ValidationError):
        ProjectEvent(**data)


def test_project_event_rejects_unknown_source_type() -> None:
    with pytest.raises(ValidationError):
        ProjectEvent(
            event_id="EVT-001",
            project_id="PROJ-001",
            source_type="slack",
            source_id="MSG-001",
            content="Deployment delayed.",
            occurred_at=datetime.now(UTC),
        )