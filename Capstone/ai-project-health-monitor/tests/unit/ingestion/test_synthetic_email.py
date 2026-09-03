import json
from pathlib import Path

from ai_project_health_monitor.ingestion.connectors.synthetic_email import (
    SyntheticEmailConnector,
)


def test_synthetic_email_connector_returns_project_events(
    tmp_path: Path,
) -> None:
    source = tmp_path / "events.json"
    source.write_text(
        json.dumps(
            [
                {
                    "event_id": "EVT-001",
                    "project_id": "PROJ-001",
                    "message_id": "EMAIL-001",
                    "subject": "Payment integration blocked",
                    "sender": "client@example.com",
                    "recipient": "team@example.com",
                    "content": "Payment integration is blocked.",
                    "occurred_at": "2026-09-02T11:00:00Z",
                }
            ]
        ),
        encoding="utf-8",
    )

    connector = SyntheticEmailConnector(source)

    events = connector.fetch_events("PROJ-001")

    assert len(events) == 1
    assert events[0].event_id == "EVT-001"
    assert events[0].source_type.value == "email"
    assert events[0].source_id == "EMAIL-001"
    assert events[0].author == "client@example.com"
    assert events[0].metadata["subject"] == "Payment integration blocked"


def test_synthetic_email_connector_filters_by_project(
    tmp_path: Path,
) -> None:
    source = tmp_path / "events.json"
    source.write_text(
        json.dumps(
            [
                {
                    "event_id": "EVT-001",
                    "project_id": "PROJ-001",
                    "message_id": "EMAIL-001",
                    "content": "Project one update.",
                    "occurred_at": "2026-09-02T11:00:00Z",
                },
                {
                    "event_id": "EVT-002",
                    "project_id": "PROJ-002",
                    "message_id": "EMAIL-002",
                    "content": "Project two update.",
                    "occurred_at": "2026-09-02T12:00:00Z",
                },
            ]
        ),
        encoding="utf-8",
    )

    connector = SyntheticEmailConnector(source)

    events = connector.fetch_events("PROJ-001")

    assert len(events) == 1
    assert events[0].project_id == "PROJ-001"


def test_synthetic_email_connector_rejects_non_array_source(
    tmp_path: Path,
) -> None:
    source = tmp_path / "events.json"
    source.write_text(
        json.dumps({"event_id": "EVT-001"}),
        encoding="utf-8",
    )

    connector = SyntheticEmailConnector(source)

    try:
        connector.fetch_events("PROJ-001")
    except ValueError as exc:
        assert str(exc) == "Synthetic email source must contain a JSON array."
    else:
        raise AssertionError("Expected ValueError")