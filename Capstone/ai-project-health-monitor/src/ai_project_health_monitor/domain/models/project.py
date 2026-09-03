from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field


class ProjectStatus(StrEnum):
    """Supported project statuses."""

    PLANNED = "planned"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(BaseModel):
    """Core project identity and lifecycle information."""

    project_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str | None = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    start_date: date | None = None
    target_end_date: date | None = None
    actual_end_date: date | None = None