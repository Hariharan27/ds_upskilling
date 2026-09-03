import json
from pathlib import Path
from typing import Any

from ai_project_health_monitor.domain.models.project_event import (
    ProjectEvent,
    SourceType,
)
from ai_project_health_monitor.ingestion.connectors.base import (
    ProjectSourceConnector,
)
from ai_project_health_monitor.ingestion.normalizer import EventNormalizer


class SyntheticJiraNormalizer(EventNormalizer):
    """Normalize synthetic JIRA events into ProjectEvent objects."""

    def normalize(self, raw_event: dict[str, Any]) -> ProjectEvent:
        return ProjectEvent(
            event_id=raw_event["event_id"],
            project_id=raw_event["project_id"],
            source_type=SourceType.JIRA,
            source_id=raw_event["issue_key"],
            content=raw_event["content"],
            author=raw_event.get("author"),
            occurred_at=raw_event["occurred_at"],
            metadata={
                "status": raw_event.get("status", ""),
                "priority": raw_event.get("priority", ""),
            },
        )


class SyntheticJiraConnector(ProjectSourceConnector):
    """Read synthetic JIRA events from a JSON file."""

    def __init__(
        self,
        source_path: Path,
        normalizer: EventNormalizer | None = None,
    ) -> None:
        self._source_path = source_path
        self._normalizer = normalizer or SyntheticJiraNormalizer()

    def fetch_events(self, project_id: str) -> list[ProjectEvent]:
        raw_events = self._load_events()

        return [
            self._normalizer.normalize(event)
            for event in raw_events
            if event.get("project_id") == project_id
        ]

    def _load_events(self) -> list[dict[str, Any]]:
        with self._source_path.open(encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Synthetic JIRA source must contain a JSON array.")

        return data