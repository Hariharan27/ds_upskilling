from datetime import datetime

from pydantic import BaseModel, Field

from ai_project_health_monitor.domain.models.project_event import SourceType


class Evidence(BaseModel):
    """Source evidence supporting an AI-generated project insight."""

    source_type: SourceType
    source_id: str = Field(min_length=1)

    content: str = Field(min_length=1)

    occurred_at: datetime