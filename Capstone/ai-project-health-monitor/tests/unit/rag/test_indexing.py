from datetime import UTC, datetime

import pytest

from ai_project_health_monitor.domain.models.project_event import (
    ProjectEvent,
    SourceType,
)
from ai_project_health_monitor.rag.chunking import Chunker
from ai_project_health_monitor.rag.embeddings.base import EmbeddingModel
from ai_project_health_monitor.rag.indexing import RAGIndexer
from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.vector_store.base import VectorStore


class FakeChunker(Chunker):
    """Deterministic chunker for indexing tests."""

    def chunk(self, event: ProjectEvent) -> list[DocumentChunk]:
        return [
            DocumentChunk(
                chunk_id=f"{event.event_id}-CHUNK-001",
                project_id=event.project_id,
                event_id=event.event_id,
                source_type=event.source_type,
                source_id=event.source_id,
                content=event.content,
                chunk_index=0,
                occurred_at=event.occurred_at,
            )
        ]


class FakeEmbeddingModel(EmbeddingModel):
    """Deterministic embedding model for indexing tests."""

    def __init__(self) -> None:
        self.received_texts: list[str] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.received_texts.extend(texts)
        return [[1.0, 0.0, 0.0] for _ in texts]


class FakeVectorStore(VectorStore):
    """Deterministic vector store for indexing tests."""

    def __init__(self) -> None:
        self.received_chunks: list[DocumentChunk] = []
        self.received_embeddings: list[list[float]] = []

    def upsert(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        self.received_chunks = chunks
        self.received_embeddings = embeddings

    def search(
        self,
        query_embedding: list[float],
        project_id: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:
        return []


@pytest.fixture
def project_event() -> ProjectEvent:
    return ProjectEvent(
        event_id="EVT-001",
        project_id="PROJ-001",
        source_type=SourceType.JIRA,
        source_id="PROJ-101",
        content="Payment API integration is blocked.",
        author="developer@example.com",
        occurred_at=datetime(
            2026,
            9,
            1,
            tzinfo=UTC,
        ),
    )


@pytest.fixture
def chunker() -> FakeChunker:
    return FakeChunker()


@pytest.fixture
def embedding_model() -> FakeEmbeddingModel:
    return FakeEmbeddingModel()


@pytest.fixture
def vector_store() -> FakeVectorStore:
    return FakeVectorStore()


@pytest.fixture
def indexer(
    chunker: FakeChunker,
    embedding_model: FakeEmbeddingModel,
    vector_store: FakeVectorStore,
) -> RAGIndexer:
    return RAGIndexer(
        chunker=chunker,
        embedding_model=embedding_model,
        vector_store=vector_store,
    )


def test_index_chunks_embeds_and_stores_events(
    indexer: RAGIndexer,
    project_event: ProjectEvent,
    embedding_model: FakeEmbeddingModel,
    vector_store: FakeVectorStore,
) -> None:
    indexed_count = indexer.index([project_event])

    assert indexed_count == 1

    assert embedding_model.received_texts == [
        "Payment API integration is blocked."
    ]

    assert len(vector_store.received_chunks) == 1
    assert vector_store.received_chunks[0].event_id == "EVT-001"

    assert vector_store.received_embeddings == [
        [1.0, 0.0, 0.0]
    ]


def test_index_handles_multiple_events(
    indexer: RAGIndexer,
    embedding_model: FakeEmbeddingModel,
    vector_store: FakeVectorStore,
) -> None:
    events = [
        ProjectEvent(
            event_id="EVT-001",
            project_id="PROJ-001",
            source_type=SourceType.JIRA,
            source_id="PROJ-101",
            content="Payment integration is blocked.",
            occurred_at=datetime(
                2026,
                9,
                1,
                tzinfo=UTC,
            ),
        ),
        ProjectEvent(
            event_id="EVT-002",
            project_id="PROJ-001",
            source_type=SourceType.EMAIL,
            source_id="EMAIL-001",
            content="Client is concerned about the release.",
            occurred_at=datetime(
                2026,
                9,
                2,
                tzinfo=UTC,
            ),
        ),
    ]

    indexed_count = indexer.index(events)

    assert indexed_count == 2
    assert len(embedding_model.received_texts) == 2
    assert len(vector_store.received_chunks) == 2
    assert len(vector_store.received_embeddings) == 2


def test_index_empty_events_is_noop(
    indexer: RAGIndexer,
    embedding_model: FakeEmbeddingModel,
    vector_store: FakeVectorStore,
) -> None:
    indexed_count = indexer.index([])

    assert indexed_count == 0
    assert embedding_model.received_texts == []
    assert vector_store.received_chunks == []
    assert vector_store.received_embeddings == []


def test_index_does_not_store_when_embedding_count_mismatches(
    project_event: ProjectEvent,
    chunker: FakeChunker,
    vector_store: FakeVectorStore,
) -> None:
    class InvalidEmbeddingModel(EmbeddingModel):
        def embed(self, texts: list[str]) -> list[list[float]]:
            return []

    indexer = RAGIndexer(
        chunker=chunker,
        embedding_model=InvalidEmbeddingModel(),
        vector_store=vector_store,
    )

    with pytest.raises(
        ValueError,
        match="one vector per chunk",
    ):
        indexer.index([project_event])

    assert vector_store.received_chunks == []
    assert vector_store.received_embeddings == []