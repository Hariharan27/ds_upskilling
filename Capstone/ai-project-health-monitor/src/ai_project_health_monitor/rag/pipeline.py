from ai_project_health_monitor.ingestion.service import IngestionService
from ai_project_health_monitor.rag.indexing import RAGIndexer
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.retrieval import RetrievalService


class RAGPipeline:
    """Coordinate project ingestion, indexing, and retrieval."""

    def __init__(
        self,
        ingestion_service: IngestionService,
        indexer: RAGIndexer,
        retrieval_service: RetrievalService,
    ) -> None:
        self._ingestion_service = ingestion_service
        self._indexer = indexer
        self._retrieval_service = retrieval_service

    def index_project(self, project_id: str) -> int:
        """Ingest and index all events belonging to a project."""
        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        events = self._ingestion_service.ingest_project(project_id)

        return self._indexer.index(events)

    def retrieve(
        self,
        query: str,
        project_id: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:
        """Retrieve relevant evidence for a project query."""
        if not query.strip():
            raise ValueError("query cannot be empty")

        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        return self._retrieval_service.retrieve(
            query=query,
            project_id=project_id,
            limit=limit,
        )