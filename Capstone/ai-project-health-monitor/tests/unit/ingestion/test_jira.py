from datetime import datetime, timezone

import httpx

from ai_project_health_monitor.ingestion.connectors.jira import JiraConnector


def test_jira_connector_returns_project_events() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/rest/api/3/search/jql"
        assert request.headers["Accept"] == "application/json"

        return httpx.Response(
            200,
            json={
                "issues": [
                    {
                        "id": "10001",
                        "key": "PROJ-101",
                        "fields": {
                            "summary": "Payment API integration",
                            "description": "Payment integration is blocked.",
                            "status": {"name": "Blocked"},
                            "priority": {"name": "High"},
                            "assignee": {"displayName": "Developer One"},
                            "reporter": {"displayName": "Project Manager"},
                            "created": "2026-09-01T09:00:00.000+0000",
                            "updated": "2026-09-01T10:30:00.000+0000",
                        },
                    }
                ]
            },
        )
    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        auth=("test@example.com", "test-token"),
        headers={
            "Accept": "application/json",
        },
    )

    connector = JiraConnector(
        base_url="https://example.atlassian.net",
        email="test@example.com",
        api_token="test-token",
        project_key="PROJ",
        client=client,
    )

    events = connector.fetch_events("PROJ-001")

    assert len(events) == 1

    event = events[0]

    assert event.event_id == "jira-10001"
    assert event.project_id == "PROJ-001"
    assert event.source_id == "PROJ-101"
    assert event.content.startswith("JIRA issue: PROJ-101")
    assert "Payment integration is blocked." in event.content
    assert event.metadata["status"] == "Blocked"
    assert event.metadata["priority"] == "High"
    assert event.metadata["assignee"] == "Developer One"
    assert event.metadata["reporter"] == "Project Manager"
    assert event.author == "Project Manager"
    assert event.occurred_at == datetime(
        2026,
        9,
        1,
        10,
        30,
        tzinfo=timezone.utc,
    )


def test_jira_connector_extracts_adf_description() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "issues": [
                    {
                        "id": "10002",
                        "key": "PROJ-102",
                        "fields": {
                            "summary": "Release readiness",
                            "description": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": "Release is at risk.",
                                            }
                                        ],
                                    }
                                ],
                            },
                            "status": {"name": "In Progress"},
                            "priority": {"name": "Medium"},
                            "updated": "2026-09-02T12:00:00.000+0000",
                        },
                    }
                ]
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))

    connector = JiraConnector(
        base_url="https://example.atlassian.net",
        email="test@example.com",
        api_token="test-token",
        project_key="PROJ",
        client=client,
    )

    events = connector.fetch_events("PROJ-001")

    assert len(events) == 1
    assert "Release is at risk." in events[0].content


def test_jira_connector_raises_for_http_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            401,
            json={"errorMessages": ["Unauthorized"]},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))

    connector = JiraConnector(
        base_url="https://example.atlassian.net",
        email="test@example.com",
        api_token="invalid-token",
        project_key="PROJ",
        client=client,
    )

    try:
        connector.fetch_events("PROJ-001")
    except httpx.HTTPStatusError as exc:
        assert exc.response.status_code == 401
    else:
        raise AssertionError("Expected HTTPStatusError")


def test_jira_connector_rejects_empty_project_id() -> None:
    client = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={"issues": []})
        )
    )

    connector = JiraConnector(
        base_url="https://example.atlassian.net",
        email="test@example.com",
        api_token="test-token",
        project_key="PROJ",
        client=client,
    )

    try:
        connector.fetch_events("")
    except ValueError as exc:
        assert str(exc) == "project_id cannot be empty"
    else:
        raise AssertionError("Expected ValueError")