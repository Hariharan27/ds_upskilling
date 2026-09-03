import json
from pathlib import Path

from ai_project_health_monitor.ingestion.connectors.synthetic_jira import (
    SyntheticJiraConnector,
)


def test_synthetic_jira_connector_returns_project_events(
    tmp_path: Path,
) -> None:
    source = tmp_path / "events.json"
    source.write_text(
        json.dumps(
            [
                {
                    "event_id": "EVT-001",
                    "project_id": "PROJ-001",
                    "issue_key": "PROJ-101",
                    "status": "blocked",
                    "priority": "high",
                    "content": "Payment API is blocked.",
                    "author": "developer@example.com",
                    "occurred_at": "2026-09-01T09:30:00Z",
                }
            ]
        ),
        encoding="utf-8",
    )

    connector = SyntheticJiraConnector(source)

    events = connector.fetch_events("PROJ-001")

    assert len(events) == 1
    assert events[0].event_id == "EVT-001"
    assert events[0].project_id == "PROJ-001"
    assert events[0].source_id == "PROJ-101"
    assert events[0].content == "Payment API is blocked."
    assert events[0].metadata["status"] == "blocked"


def test_synthetic_jira_connector_filters_by_project(
    tmp_path: Path,
) -> None:
    source = tmp_path / "events.json"
    source.write_text(
        json.dumps(
            [
                {
                    "event_id": "EVT-001",
                    "project_id": "PROJ-001",
                    "issue_key": "PROJ-101",
                    "content": "Project one update.",
                    "occurred_at": "2026-09-01T09:30:00Z",
                },
                {
                    "event_id": "EVT-002",
                    "project_id": "PROJ-002",
                    "issue_key": "PROJ-201",
                    "content": "Project two update.",
                    "occurred_at": "2026-09-01T10:30:00Z",
                },
            ]
        ),
        encoding="utf-8",
    )

    connector = SyntheticJiraConnector(source)

    events = connector.fetch_events("PROJ-001")

    assert len(events) == 1
    assert events[0].project_id == "PROJ-001"


def test_synthetic_jira_connector_rejects_non_array_source(
    tmp_path: Path,
) -> None:
    source = tmp_path / "events.json"
    source.write_text(
        json.dumps({"event_id": "EVT-001"}),
        encoding="utf-8",
    )

    connector = SyntheticJiraConnector(source)

    try:
        connector.fetch_events("PROJ-001")
    except ValueError as exc:
        assert str(exc) == "Synthetic JIRA source must contain a JSON array."
    else:
        raise AssertionError("Expected ValueError")