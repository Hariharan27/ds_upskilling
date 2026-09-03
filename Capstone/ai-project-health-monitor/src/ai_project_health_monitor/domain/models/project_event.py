from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class SourceType(StrEnum):
    """Supported source types for project events."""

    JIRA = "jira"
    EMAIL = "email"
    DOCUMENT = "document"


class ProjectEvent(BaseModel):
    """Normalized project information received from an external source."""

    event_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)

    source_type: SourceType
    source_id: str = Field(min_length=1)

    content: str = Field(min_length=1)

    author: str | None = None
    occurred_at: datetime

    metadata: dict[str, str] = Field(default_factory=dict)