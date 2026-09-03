from abc import ABC, abstractmethod

from ai_project_health_monitor.domain.models.project_event import ProjectEvent


class ProjectSourceConnector(ABC):
    """Interface for project information source connectors."""

    @abstractmethod
    def fetch_events(self, project_id: str) -> list[ProjectEvent]:
        """Fetch normalized project events for a project."""
        raise NotImplementedError