from datetime import UTC, datetime
from pathlib import Path

from ai_project_health_monitor.domain.models.project_event import (
    ProjectEvent,
    SourceType,
)
from ai_project_health_monitor.ingestion.connectors.base import (
    ProjectSourceConnector,
)


class SyntheticDocumentConnector(ProjectSourceConnector):
    """Read synthetic project documents from a directory."""

    def __init__(self, source_directory: Path) -> None:
        self._source_directory = source_directory

    def fetch_events(self, project_id: str) -> list[ProjectEvent]:
        events: list[ProjectEvent] = []

        for document_path in sorted(self._source_directory.glob("*.md")):
            content = document_path.read_text(encoding="utf-8")

            if not content.strip():
                continue

            events.append(
                ProjectEvent(
                    event_id=f"DOC-EVENT-{document_path.stem}",
                    project_id=project_id,
                    source_type=SourceType.DOCUMENT,
                    source_id=document_path.name,
                    content=content,
                    occurred_at=datetime.fromtimestamp(
                        document_path.stat().st_mtime,
                        tz=UTC,
                    ),
                    metadata={
                        "file_name": document_path.name,
                        "file_type": "markdown",
                    },
                )
            )

        return events