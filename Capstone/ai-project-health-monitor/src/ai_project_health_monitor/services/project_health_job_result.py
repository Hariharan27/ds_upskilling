from pydantic import BaseModel, Field

from ai_project_health_monitor.orchestration.state import ProjectHealthState


class ProjectHealthJobResult(BaseModel):
    """Result of one end-to-end project health monitoring job."""

    project_id: str = Field(min_length=1)
    events_ingested: int = Field(ge=0)
    chunks_indexed: int = Field(ge=0)
    evidence_changed: bool
    health_state: ProjectHealthState