from datetime import datetime
from typing import Any

import httpx

from ai_project_health_monitor.domain.models.project_event import (
    ProjectEvent,
    SourceType,
)
from ai_project_health_monitor.ingestion.connectors.base import (
    ProjectSourceConnector,
)


class JiraConnector(ProjectSourceConnector):
    """Fetch project issues from Jira Cloud."""

    def __init__(
        self,
        base_url: str,
        email: str,
        api_token: str,
        project_key: str,
        *,
        timeout_seconds: float = 30.0,
        client: httpx.Client | None = None,
    ) -> None:
        if not base_url.strip():
            raise ValueError("JIRA base URL cannot be empty")
        if not email.strip():
            raise ValueError("JIRA email cannot be empty")
        if not api_token.strip():
            raise ValueError("JIRA API token cannot be empty")
        if not project_key.strip():
            raise ValueError("JIRA project key cannot be empty")

        self._base_url = base_url.rstrip("/")
        self._email = email
        self._api_token = api_token
        self._project_key = project_key
        self._timeout_seconds = timeout_seconds
        self._client = client

    def fetch_events(self, project_id: str) -> list[ProjectEvent]:
        """Fetch Jira issues for the configured project."""
        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        response = self._request_issues()
        data = response.json()

        issues = data.get("issues", [])
        if not isinstance(issues, list):
            raise ValueError("JIRA response contains an invalid issues field")

        return [
            self._normalize_issue(issue, project_id)
            for issue in issues
        ]

    def _request_issues(self) -> httpx.Response:
        url = f"{self._base_url}/rest/api/3/search/jql"

        response = self._get_client().get(
            url,
            params={
                "jql": f"project = {self._project_key} ORDER BY updated DESC",
                "maxResults": 100,
                "fields": (
                    "summary,description,status,priority,"
                    "assignee,reporter,created,updated"
                ),
            },
        )

        response.raise_for_status()
        return response

    def _normalize_issue(
        self,
        issue: dict[str, Any],
        project_id: str,
    ) -> ProjectEvent:
        fields = issue.get("fields", {})

        if not isinstance(fields, dict):
            raise ValueError("JIRA issue contains invalid fields")

        issue_key = self._require_string(issue, "key")
        issue_id = self._require_string(issue, "id")

        occurred_at = self._parse_datetime(
            fields.get("updated") or fields.get("created")
        )

        content = self._build_content(
            issue_key=issue_key,
            fields=fields,
        )

        metadata = {
            "status": self._extract_name(fields.get("status")),
            "priority": self._extract_name(fields.get("priority")),
        }

        assignee = self._extract_display_name(fields.get("assignee"))
        if assignee is not None:
            metadata["assignee"] = assignee

        reporter = self._extract_display_name(fields.get("reporter"))
        if reporter is not None:
            metadata["reporter"] = reporter

        return ProjectEvent(
            event_id=f"jira-{issue_id}",
            project_id=project_id,
            source_type=SourceType.JIRA,
            source_id=issue_key,
            content=content,
            author=reporter,
            occurred_at=occurred_at,
            metadata=metadata,
        )

    @staticmethod
    def _build_content(
        *,
        issue_key: str,
        fields: dict[str, Any],
    ) -> str:
        summary = fields.get("summary") or ""
        description = JiraConnector._extract_description(
            fields.get("description")
        )

        parts = [
            f"JIRA issue: {issue_key}",
            f"Summary: {summary}",
        ]

        if description:
            parts.append(f"Description: {description}")

        status = JiraConnector._extract_name(fields.get("status"))
        if status:
            parts.append(f"Status: {status}")

        priority = JiraConnector._extract_name(fields.get("priority"))
        if priority:
            parts.append(f"Priority: {priority}")

        return "\n".join(parts)

    @staticmethod
    def _extract_description(description: Any) -> str:
        if isinstance(description, str):
            return description.strip()

        if not isinstance(description, dict):
            return ""

        return JiraConnector._extract_adf_text(description).strip()

    @staticmethod
    def _extract_adf_text(node: Any) -> str:
        if isinstance(node, dict):
            parts: list[str] = []

            text = node.get("text")
            if isinstance(text, str):
                parts.append(text)

            content = node.get("content")
            if isinstance(content, list):
                for child in content:
                    parts.append(JiraConnector._extract_adf_text(child))

            return " ".join(part for part in parts if part)

        if isinstance(node, list):
            return " ".join(
                JiraConnector._extract_adf_text(child)
                for child in node
            )

        return ""

    @staticmethod
    def _extract_name(value: Any) -> str:
        if isinstance(value, dict):
            name = value.get("name")
            if isinstance(name, str):
                return name

        return ""

    @staticmethod
    def _extract_display_name(value: Any) -> str | None:
        if isinstance(value, dict):
            display_name = value.get("displayName")
            if isinstance(display_name, str):
                return display_name

        return None

    @staticmethod
    def _require_string(
        value: dict[str, Any],
        field: str,
    ) -> str:
        result = value.get(field)

        if not isinstance(result, str) or not result.strip():
            raise ValueError(f"JIRA issue is missing required field: {field}")

        return result

    @staticmethod
    def _parse_datetime(value: Any) -> datetime:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("JIRA issue is missing updated/created timestamp")

        return datetime.fromisoformat(
            value.replace("Z", "+00:00").replace("+0000", "+00:00")
        )

    def _get_client(self) -> httpx.Client:
        if self._client is not None:
            return self._client

        return httpx.Client(
            auth=(self._email, self._api_token),
            timeout=self._timeout_seconds,
            headers={
                "Accept": "application/json",
            },
        )