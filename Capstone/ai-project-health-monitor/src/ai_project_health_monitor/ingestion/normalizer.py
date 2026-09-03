from abc import ABC, abstractmethod
from typing import Any

from ai_project_health_monitor.domain.models.project_event import ProjectEvent


class EventNormalizer(ABC):
    """Interface for converting source data into ProjectEvent objects."""

    @abstractmethod
    def normalize(self, raw_event: dict[str, Any]) -> ProjectEvent:
        """Convert a raw source event into a canonical project event."""
        raise NotImplementedError