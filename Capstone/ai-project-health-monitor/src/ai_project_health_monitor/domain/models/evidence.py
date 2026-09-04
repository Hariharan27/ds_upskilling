from datetime import datetime

from pydantic import BaseModel, Field

from ai_project_health_monitor.domain.models.project_event import SourceType


class Evidence(BaseModel):
    """Evidence used to support an AI-generated project decision."""

    event_id: str = Field(min_length=1)
    source_type: SourceType
    source_id: str = Field(min_length=1)
    content: str = Field(min_length=1)
    occurred_at: datetime