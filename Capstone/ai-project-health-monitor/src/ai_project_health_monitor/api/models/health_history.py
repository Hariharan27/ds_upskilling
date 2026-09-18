from datetime import datetime

from pydantic import BaseModel, Field

from ai_project_health_monitor.domain.models.health_score import HealthStatus


class HealthHistoryPoint(BaseModel):
    """Single historical health snapshot exposed to the frontend."""

    score: float = Field(ge=0.0, le=100.0)
    status: HealthStatus
    calculated_at: datetime


class HealthHistoryResponse(BaseModel):
    """Historical health scores for a project."""

    project_id: str = Field(min_length=1)
    points: list[HealthHistoryPoint] = Field(default_factory=list)