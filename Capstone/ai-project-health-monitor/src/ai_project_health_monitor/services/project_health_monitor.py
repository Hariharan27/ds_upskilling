from langgraph.graph.state import CompiledStateGraph

from ai_project_health_monitor.domain.models.health_trend import HealthTrend
from ai_project_health_monitor.domain.models.project_event import ProjectEvent
from ai_project_health_monitor.orchestration.state import ProjectHealthState
from ai_project_health_monitor.rag.indexing import RAGIndexer
from ai_project_health_monitor.services.health_trend_service import (
    HealthTrendService,
)
from ai_project_health_monitor.services.project_health_job_result import (
    ProjectHealthJobResult,
)
from ai_project_health_monitor.ingestion.service import IngestionService


class ProjectHealthMonitor:
    """Application service for running a project health assessment."""

    def __init__(
        self,
        graph: CompiledStateGraph[
            ProjectHealthState,
            None,
            ProjectHealthState,
            ProjectHealthState,
        ],
        health_trend_service: HealthTrendService,
        ingestion_service: IngestionService,
        rag_indexer: RAGIndexer,
    ) -> None:
        self._graph = graph
        self._health_trend_service = health_trend_service
        self._ingestion_service = ingestion_service
        self._rag_indexer = rag_indexer

    def analyze(self, project_id: str) -> ProjectHealthState:
        """Run the project health workflow for a project."""
        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        state = ProjectHealthState(
            project_id=project_id,
            query="project health assessment",
        )

        result = self._graph.invoke(state)
        return ProjectHealthState.model_validate(result)

    def run_job(self, project_id: str) -> ProjectHealthJobResult:
        """Run the complete ingestion, indexing, and health monitoring job."""
        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        events: list[ProjectEvent] = self._ingestion_service.ingest_project(
            project_id
        )

        chunks_indexed = self._rag_indexer.index(events)

        health_state = self.analyze(project_id)

        return ProjectHealthJobResult(
            project_id=project_id,
            events_ingested=len(events),
            chunks_indexed=chunks_indexed,
            evidence_changed=health_state.evidence_changed,
            health_state=health_state,
        )

    def get_trend(self, project_id: str) -> HealthTrend | None:
        """Return the historical health trend for a project."""
        return self._health_trend_service.get_trend(project_id)