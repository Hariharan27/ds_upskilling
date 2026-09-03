from datetime import UTC, datetime
from typing import Any

import pytest

from ai_project_health_monitor.domain.models.project_event import (
    ProjectEvent,
    SourceType,
)
from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.pipeline import RAGPipeline


class FakeIngestionService:
    """Test double for project event ingestion."""

    def __init__(self, events: list[ProjectEvent]) -> None:
        self.events = events
        self.received_project_id: str | None = None

    def ingest_project(self, project_id: str) -> list[ProjectEvent]:
        self.received_project_id = project_id
        return self.events


class FakeIndexer:
    """Test double for RAG indexing."""

    def __init__(self, indexed_count: int) -> None:
        self.indexed_count = indexed_count
        self.received_events: list[ProjectEvent] | None = None

    def index(self, events: list[ProjectEvent]) -> int:
        self.received_events = events
        return self.indexed_count


class FakeRetrievalService:
    """Test double for semantic retrieval."""

    def __init__(self, results: list[RetrievalResult]) -> None:
        self.results = results
        self.received_query: str | None = None
        self.received_project_id: str | None = None
        self.received_limit: int | None = None

    def retrieve(
        self,
        query: str,
        project_id: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:
        self.received_query = query
        self.received_project_id = project_id
        self.received_limit = limit
        return self.results


@pytest.fixture
def project_event() -> ProjectEvent:
    return ProjectEvent(
        event_id="EVT-001",
        project_id="PROJ-001",
        source_type=SourceType.JIRA,
        source_id="PROJ-101",
        content="Payment API integration is blocked.",
        occurred_at=datetime(
            2026,
            9,
            1,
            tzinfo=UTC,
        ),
    )


@pytest.fixture
def retrieval_result(project_event: ProjectEvent) -> RetrievalResult:
    chunk = DocumentChunk(
        chunk_id="EVT-001-CHUNK-000",
        project_id=project_event.project_id,
        event_id=project_event.event_id,
        source_type=project_event.source_type,
        source_id=project_event.source_id,
        content=project_event.content,
        chunk_index=0,
        occurred_at=project_event.occurred_at,
    )

    return RetrievalResult(
        chunk=chunk,
        score=0.92,
    )


@pytest.fixture
def pipeline(
    project_event: ProjectEvent,
) -> tuple[
    RAGPipeline,
    FakeIngestionService,
    FakeIndexer,
    FakeRetrievalService,
]:
    ingestion_service = FakeIngestionService([project_event])
    indexer = FakeIndexer(indexed_count=1)
    retrieval_service = FakeRetrievalService([])

    pipeline = RAGPipeline(
        ingestion_service=ingestion_service,  # type: ignore[arg-type]
        indexer=indexer,  # type: ignore[arg-type]
        retrieval_service=retrieval_service,  # type: ignore[arg-type]
    )

    return (
        pipeline,
        ingestion_service,
        indexer,
        retrieval_service,
    )


def test_index_project_ingests_and_indexes_events(
    pipeline: tuple[
        RAGPipeline,
        FakeIngestionService,
        FakeIndexer,
        FakeRetrievalService,
    ],
    project_event: ProjectEvent,
) -> None:
    rag_pipeline, ingestion_service, indexer, _ = pipeline

    indexed_count = rag_pipeline.index_project("PROJ-001")

    assert indexed_count == 1
    assert ingestion_service.received_project_id == "PROJ-001"
    assert indexer.received_events == [project_event]


def test_index_project_returns_zero_when_no_events() -> None:
    ingestion_service = FakeIngestionService([])
    indexer = FakeIndexer(indexed_count=0)
    retrieval_service = FakeRetrievalService([])

    pipeline = RAGPipeline(
        ingestion_service=ingestion_service,  # type: ignore[arg-type]
        indexer=indexer,  # type: ignore[arg-type]
        retrieval_service=retrieval_service,  # type: ignore[arg-type]
    )

    indexed_count = pipeline.index_project("PROJ-001")

    assert indexed_count == 0
    assert indexer.received_events == []


def test_retrieve_forwards_parameters(
    retrieval_result: RetrievalResult,
) -> None:
    ingestion_service = FakeIngestionService([])
    indexer = FakeIndexer(indexed_count=0)
    retrieval_service = FakeRetrievalService([retrieval_result])

    pipeline = RAGPipeline(
        ingestion_service=ingestion_service,  # type: ignore[arg-type]
        indexer=indexer,  # type: ignore[arg-type]
        retrieval_service=retrieval_service,  # type: ignore[arg-type]
    )

    results = pipeline.retrieve(
        query="Why is the payment integration blocked?",
        project_id="PROJ-001",
        limit=3,
    )

    assert results == [retrieval_result]
    assert retrieval_service.received_query == (
        "Why is the payment integration blocked?"
    )
    assert retrieval_service.received_project_id == "PROJ-001"
    assert retrieval_service.received_limit == 3


@pytest.mark.parametrize(
    ("method", "args", "message"),
    [
        (
            "index_project",
            ("",),
            "project_id cannot be empty",
        ),
        (
            "index_project",
            ("   ",),
            "project_id cannot be empty",
        ),
        (
            "retrieve",
            ("", "PROJ-001", 5),
            "query cannot be empty",
        ),
        (
            "retrieve",
            ("   ", "PROJ-001", 5),
            "query cannot be empty",
        ),
        (
            "retrieve",
            ("test query", "", 5),
            "project_id cannot be empty",
        ),
        (
            "retrieve",
            ("test query", "   ", 5),
            "project_id cannot be empty",
        ),
        (
            "retrieve",
            ("test query", "PROJ-001", 0),
            "limit must be greater than zero",
        ),
        (
            "retrieve",
            ("test query", "PROJ-001", -1),
            "limit must be greater than zero",
        ),
    ],
)
def test_pipeline_rejects_invalid_input(
    pipeline: tuple[
        RAGPipeline,
        FakeIngestionService,
        FakeIndexer,
        FakeRetrievalService,
    ],
    method: str,
    args: tuple[Any, ...],
    message: str,
) -> None:
    rag_pipeline, _, _, _ = pipeline

    with pytest.raises(ValueError, match=message):
        getattr(rag_pipeline, method)(*args)