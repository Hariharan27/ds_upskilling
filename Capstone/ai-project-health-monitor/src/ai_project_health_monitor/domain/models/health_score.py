from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class HealthStatus(StrEnum):
    """Overall project health classification."""

    HEALTHY = "healthy"
    AT_RISK = "at_risk"
    CRITICAL = "critical"


class HealthScore(BaseModel):
    """Explainable project health score."""

    project_id: str = Field(min_length=1)

    score: float = Field(ge=0.0, le=100.0)

    status: HealthStatus

    contributing_risks: list[str] = Field(default_factory=list)

    calculated_at: datetime

    rationale: str = Field(min_length=1)