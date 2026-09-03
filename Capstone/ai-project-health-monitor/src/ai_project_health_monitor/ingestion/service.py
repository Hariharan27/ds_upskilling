from ai_project_health_monitor.domain.models.project_event import ProjectEvent
from ai_project_health_monitor.ingestion.connectors.base import (
    ProjectSourceConnector,
)


class IngestionService:
    """Orchestrates project event ingestion from multiple sources."""

    def __init__(
        self,
        connectors: list[ProjectSourceConnector],
    ) -> None:
        self._connectors = connectors

    def ingest_project(self, project_id: str) -> list[ProjectEvent]:
        """Collect events from all configured project source connectors."""
        events: list[ProjectEvent] = []

        for connector in self._connectors:
            events.extend(connector.fetch_events(project_id))

        return sorted(
            events,
            key=lambda event: event.occurred_at,
        )