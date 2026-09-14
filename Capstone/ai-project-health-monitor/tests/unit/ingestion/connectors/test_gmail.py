import base64
from datetime import UTC, datetime
from pathlib import Path

from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.ingestion.connectors.gmail import GmailConnector


def test_to_project_event_maps_gmail_message() -> None:
    body = (
        "Payment gateway integration is blocked because "
        "merchant approval is still pending."
    )
    encoded_body = base64.urlsafe_b64encode(
        body.encode("utf-8")
    ).decode("utf-8")

    message = {
        "id": "msg-001",
        "threadId": "thread-001",
        "payload": {
            "headers": [
                {
                    "name": "From",
                    "value": "manager@example.com",
                },
                {
                    "name": "To",
                    "value": "team@example.com",
                },
                {
                    "name": "Subject",
                    "value": "Payment integration update",
                },
                {
                    "name": "Date",
                    "value": "Tue, 15 Sep 2026 10:30:00 +0530",
                },
            ],
            "body": {
                "data": encoded_body,
            },
        },
    }

    event = GmailConnector._to_project_event(
        project_id="AIPHM",
        message=message,
    )

    assert event is not None
    assert event.event_id == "gmail-msg-001"
    assert event.project_id == "AIPHM"
    assert event.source_type == SourceType.EMAIL
    assert event.source_id == "msg-001"
    assert event.content == body
    assert event.author == "manager@example.com"
    assert event.occurred_at == datetime(
        2026,
        9,
        15,
        5,
        0,
        tzinfo=UTC,
    )
    assert event.metadata == {
        "subject": "Payment integration update",
        "recipient": "team@example.com",
        "thread_id": "thread-001",
    }


def test_extract_body_handles_nested_multipart_message() -> None:
    body = "The release is at risk because testing is delayed."
    encoded_body = base64.urlsafe_b64encode(
        body.encode("utf-8")
    ).decode("utf-8")

    payload = {
        "parts": [
            {
                "mimeType": "text/plain",
                "body": {
                    "data": encoded_body,
                },
            }
        ]
    }

    assert GmailConnector._extract_body(payload) == body


def test_to_project_event_returns_none_without_body() -> None:
    message = {
        "id": "msg-002",
        "payload": {
            "headers": [],
            "body": {},
        },
    }

    event = GmailConnector._to_project_event(
        project_id="AIPHM",
        message=message,
    )

    assert event is None


def test_connector_rejects_empty_project_id(tmp_path: Path) -> None:
    connector = GmailConnector(
        credentials_path=tmp_path / "credentials.json",
        token_path=tmp_path / "token.json",
    )

    try:
        connector.fetch_events("   ")
    except ValueError as exc:
        assert str(exc) == "project_id cannot be empty"
    else:
        raise AssertionError("Expected ValueError")