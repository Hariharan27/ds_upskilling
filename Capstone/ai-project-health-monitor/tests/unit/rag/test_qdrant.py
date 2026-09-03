from datetime import UTC, datetime

import pytest
from qdrant_client import QdrantClient

from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.vector_store.qdrant import QdrantVectorStore

VECTOR_SIZE = 3


@pytest.fixture
def vector_store() -> QdrantVectorStore:
    """Create an isolated in-memory Qdrant vector store."""
    client = QdrantClient(":memory:")

    return QdrantVectorStore(
        client=client,
        vector_size=VECTOR_SIZE,
    )


def create_chunk(
    chunk_id: str,
    project_id: str,
    content: str,
    chunk_index: int,
) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        project_id=project_id,
        event_id=f"EVT-{project_id}",
        source_type=SourceType.JIRA,
        source_id=f"{project_id}-101",
        content=content,
        chunk_index=chunk_index,
        occurred_at=datetime(
            2026,
            9,
            1,
            tzinfo=UTC,
        ),
    )


def test_upsert_and_search_returns_matching_chunks(
    vector_store: QdrantVectorStore,
) -> None:
    chunks = [
        create_chunk(
            "CHUNK-001",
            "PROJ-001",
            "Payment API integration is blocked.",
            0,
        ),
        create_chunk(
            "CHUNK-002",
            "PROJ-001",
            "Backend development is three days behind.",
            1,
        ),
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
    ]

    vector_store.upsert(chunks, embeddings)

    results = vector_store.search(
        query_embedding=[1.0, 0.0, 0.0],
        project_id="PROJ-001",
        limit=2,
    )

    assert len(results) == 2
    assert results[0].chunk.chunk_id == "CHUNK-001"
    assert results[1].chunk.chunk_id == "CHUNK-002"


def test_search_filters_by_project(
    vector_store: QdrantVectorStore,
) -> None:
    chunks = [
        create_chunk(
            "CHUNK-001",
            "PROJ-001",
            "Payment API integration is blocked.",
            0,
        ),
        create_chunk(
            "CHUNK-002",
            "PROJ-002",
            "Reporting module completed successfully.",
            0,
        ),
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.99, 0.01, 0.0],
    ]

    vector_store.upsert(chunks, embeddings)

    results = vector_store.search(
        query_embedding=[1.0, 0.0, 0.0],
        project_id="PROJ-001",
        limit=5,
    )

    assert len(results) == 1
    assert results[0].chunk.project_id == "PROJ-001"
    assert results[0].chunk.chunk_id == "CHUNK-001"


def test_search_respects_limit(
    vector_store: QdrantVectorStore,
) -> None:
    chunks = [
        create_chunk(
            "CHUNK-001",
            "PROJ-001",
            "Payment API integration is blocked.",
            0,
        ),
        create_chunk(
            "CHUNK-002",
            "PROJ-001",
            "Backend development is delayed.",
            1,
        ),
        create_chunk(
            "CHUNK-003",
            "PROJ-001",
            "Client requested additional scope.",
            2,
        ),
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
        [0.8, 0.2, 0.0],
    ]

    vector_store.upsert(chunks, embeddings)

    results = vector_store.search(
        query_embedding=[1.0, 0.0, 0.0],
        project_id="PROJ-001",
        limit=2,
    )

    assert len(results) == 2


def test_upsert_rejects_mismatched_lengths(
    vector_store: QdrantVectorStore,
) -> None:
    chunks = [
        create_chunk(
            "CHUNK-001",
            "PROJ-001",
            "Payment API integration is blocked.",
            0,
        ),
    ]

    embeddings = [
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
    ]

    with pytest.raises(
        ValueError,
        match="same length",
    ):
        vector_store.upsert(chunks, embeddings)


def test_search_rejects_invalid_limit(
    vector_store: QdrantVectorStore,
) -> None:
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        vector_store.search(
            query_embedding=[1.0, 0.0, 0.0],
            project_id="PROJ-001",
            limit=0,
        )


def test_constructor_rejects_invalid_vector_size() -> None:
    client = QdrantClient(":memory:")

    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        QdrantVectorStore(
            client=client,
            vector_size=0,
        )