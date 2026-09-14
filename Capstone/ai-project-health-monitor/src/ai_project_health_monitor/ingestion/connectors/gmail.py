import base64
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource
from googleapiclient.discovery import build

from ai_project_health_monitor.domain.models.project_event import (
    ProjectEvent,
    SourceType,
)
from ai_project_health_monitor.ingestion.connectors.base import (
    ProjectSourceConnector,
)


class GmailConnector(ProjectSourceConnector):
    """Fetch project-related emails from Gmail using OAuth 2.0."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(
        self,
        credentials_path: Path,
        token_path: Path,
    ) -> None:
        self._credentials_path = credentials_path
        self._token_path = token_path

    def fetch_events(self, project_id: str) -> list[ProjectEvent]:
        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        service = self._build_service()

        messages = self._list_messages(
            service=service,
            project_id=project_id,
        )

        events: list[ProjectEvent] = []

        for message in messages:
            message_id = message.get("id")
            if not message_id:
                continue

            details = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="full",
                )
                .execute()
            )

            event = self._to_project_event(
                project_id=project_id,
                message=details,
            )

            if event is not None:
                events.append(event)

        return events

    def _build_service(self) -> Resource:
        credentials: Credentials | None = None

        if self._token_path.exists():
            credentials = Credentials.from_authorized_user_file(
                str(self._token_path),
                self.SCOPES,
            )

        if credentials is None or not credentials.valid:
            if (
                credentials is not None
                and credentials.expired
                and credentials.refresh_token
            ):
                from google.auth.transport.requests import Request

                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self._credentials_path),
                    self.SCOPES,
                )
                credentials = flow.run_local_server(port=0)

            self._token_path.write_text(
                credentials.to_json(),
                encoding="utf-8",
            )

        return build(
            "gmail",
            "v1",
            credentials=credentials,
        )

    @staticmethod
    def _list_messages(
        service: Resource,
        project_id: str,
    ) -> list[dict[str, Any]]:
        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=f'"{project_id}"',
            )
            .execute()
        )

        return response.get("messages", [])

    @classmethod
    def _to_project_event(
        cls,
        project_id: str,
        message: dict[str, Any],
    ) -> ProjectEvent | None:
        payload = message.get("payload", {})
        headers = payload.get("headers", [])

        header_map = {
            header.get("name", "").lower(): header.get("value", "")
            for header in headers
        }

        content = cls._extract_body(payload)

        if not content:
            return None

        occurred_at = cls._parse_date(
            header_map.get("date"),
        )

        message_id = message.get("id")
        if not message_id:
            return None

        return ProjectEvent(
            event_id=f"gmail-{message_id}",
            project_id=project_id,
            source_type=SourceType.EMAIL,
            source_id=message_id,
            content=content,
            author=header_map.get("from"),
            occurred_at=occurred_at,
            metadata={
                "subject": header_map.get("subject", ""),
                "recipient": header_map.get("to", ""),
                "thread_id": message.get("threadId", ""),
            },
        )

    @staticmethod
    def _extract_body(payload: dict[str, Any]) -> str:
        body = payload.get("body", {})
        data = body.get("data")

        if data:
            return base64.urlsafe_b64decode(data).decode(
                "utf-8",
                errors="replace",
            )

        for part in payload.get("parts", []):
            content = GmailConnector._extract_body(part)
            if content:
                return content

        return ""

    @staticmethod
    def _parse_date(value: str | None) -> datetime:
        if not value:
            return datetime.now(timezone.utc)

        try:
            parsed = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return datetime.now(timezone.utc)

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)