from datetime import datetime

from pydantic import BaseModel, Field

from ai_project_health_monitor.domain.models.project_event import SourceType


class DocumentChunk(BaseModel):
    """A retrievable chunk derived from a canonical project event."""

    chunk_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    event_id: str = Field(min_length=1)

    source_type: SourceType
    source_id: str = Field(min_length=1)

    content: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)

    occurred_at: datetime