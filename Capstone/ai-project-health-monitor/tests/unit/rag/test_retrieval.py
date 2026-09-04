from datetime import UTC, datetime

import pytest

from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.rag.embeddings.base import EmbeddingModel
from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.retrieval import RetrievalService
from ai_project_health_monitor.rag.vector_store.base import VectorStore


class FakeEmbeddingModel(EmbeddingModel):
    """Deterministic embedding model for retrieval tests."""

    def __init__(self) -> None:
        self.received_texts: list[str] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.received_texts.extend(texts)
        return [[1.0, 0.0, 0.0] for _ in texts]


class FakeVectorStore(VectorStore):
    """Deterministic vector store for retrieval tests."""

    def __init__(self) -> None:
        self.received_embedding: list[float] | None = None
        self.received_project_id: str | None = None
        self.received_limit: int | None = None
        self.results: list[RetrievalResult] = []

    def upsert(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        pass

    def search(
        self,
        query_embedding: list[float],
        project_id: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:
        self.received_embedding = query_embedding
        self.received_project_id = project_id
        self.received_limit = limit

        chunk = DocumentChunk(
            chunk_id="CHUNK-001",
            project_id=project_id,
            event_id="EVT-001",
            source_type=SourceType.JIRA,
            source_id="PROJ-101",
            content="Payment API integration is blocked.",
            chunk_index=0,
            occurred_at=datetime(
                2026,
                9,
                1,
                tzinfo=UTC,
            ),
        )

        self.results = [
            RetrievalResult(
                chunk=chunk,
                score=0.95,
            )
        ]

        return self.results

def make_result(event_id: str, score: float) -> RetrievalResult:
    """Create a deterministic retrieval result for retrieval tests."""
    chunk = DocumentChunk(
        chunk_id=f"CHUNK-{event_id}",
        project_id="PROJ-001",
        event_id=event_id,
        source_type=SourceType.JIRA,
        source_id=f"SOURCE-{event_id}",
        content=f"Content for {event_id}",
        chunk_index=0,
        occurred_at=datetime(
            2026,
            9,
            1,
            tzinfo=UTC,
        ),
    )

    return RetrievalResult(
        chunk=chunk,
        score=score,
    )


@pytest.fixture
def embedding_model() -> FakeEmbeddingModel:
    return FakeEmbeddingModel()


@pytest.fixture
def vector_store() -> FakeVectorStore:
    return FakeVectorStore()


@pytest.fixture
def retrieval_service(
    embedding_model: FakeEmbeddingModel,
    vector_store: FakeVectorStore,
) -> RetrievalService:
    return RetrievalService(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )


def test_retrieve_embeds_query_and_searches(
    retrieval_service: RetrievalService,
    embedding_model: FakeEmbeddingModel,
    vector_store: FakeVectorStore,
) -> None:
    results = retrieval_service.retrieve(
        query="Why is payment integration blocked?",
        project_id="PROJ-001",
        limit=3,
    )

    assert embedding_model.received_texts == [
        "Why is payment integration blocked?"
    ]
    assert vector_store.received_embedding == [1.0, 0.0, 0.0]
    assert vector_store.received_project_id == "PROJ-001"
    assert vector_store.received_limit == 3

    assert len(results) == 1
    assert results[0].chunk.chunk_id == "CHUNK-001"
    assert results[0].score == 0.95


def test_retrieve_rejects_empty_query(
    retrieval_service: RetrievalService,
) -> None:
    with pytest.raises(ValueError, match="query cannot be empty"):
        retrieval_service.retrieve(
            query="   ",
            project_id="PROJ-001",
        )


def test_retrieve_rejects_empty_project_id(
    retrieval_service: RetrievalService,
) -> None:
    with pytest.raises(ValueError, match="project_id cannot be empty"):
        retrieval_service.retrieve(
            query="payment issue",
            project_id="   ",
        )


def test_retrieve_rejects_invalid_limit(
    retrieval_service: RetrievalService,
) -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        retrieval_service.retrieve(
            query="payment issue",
            project_id="PROJ-001",
            limit=0,
        )


def test_retrieve_rejects_invalid_embedding_response(
    vector_store: FakeVectorStore,
) -> None:
    class InvalidEmbeddingModel(EmbeddingModel):
        def embed(self, texts: list[str]) -> list[list[float]]:
            return []

    service = RetrievalService(
        embedding_model=InvalidEmbeddingModel(),
        vector_store=vector_store,
    )

    with pytest.raises(
        ValueError,
        match="exactly one vector",
    ):
        service.retrieve(
            query="payment issue",
            project_id="PROJ-001",
        )


