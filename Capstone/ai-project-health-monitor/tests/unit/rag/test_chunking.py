from datetime import UTC, datetime

import pytest

from ai_project_health_monitor.domain.models.project_event import (
    ProjectEvent,
    SourceType,
)
from ai_project_health_monitor.rag.chunking import FixedSizeChunker


@pytest.fixture
def project_event() -> ProjectEvent:
    return ProjectEvent(
        event_id="EVT-001",
        project_id="PROJ-001",
        source_type=SourceType.JIRA,
        source_id="PROJ-101",
        content="abcdefghijklmnopqrstuvwxyz",
        author="developer@example.com",
        occurred_at=datetime(2026, 9, 1, 9, 30, tzinfo=UTC),
    )


def test_chunker_splits_content(project_event: ProjectEvent) -> None:
    chunker = FixedSizeChunker(chunk_size=10, overlap=2)

    chunks = chunker.chunk(project_event)

    assert len(chunks) == 3
    assert chunks[0].content == "abcdefghij"
    assert chunks[1].content == "ijklmnopqr"
    assert chunks[2].content == "qrstuvwxyz"
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1
    assert chunks[2].chunk_index == 2


def test_chunker_preserves_source_metadata(project_event: ProjectEvent) -> None:
    chunker = FixedSizeChunker(chunk_size=10, overlap=2)

    chunks = chunker.chunk(project_event)

    assert all(chunk.project_id == project_event.project_id for chunk in chunks)
    assert all(chunk.event_id == project_event.event_id for chunk in chunks)
    assert all(chunk.source_type == project_event.source_type for chunk in chunks)
    assert all(chunk.source_id == project_event.source_id for chunk in chunks)


def test_chunker_returns_single_chunk_for_short_content(
    project_event: ProjectEvent,
) -> None:
    chunker = FixedSizeChunker(chunk_size=100, overlap=10)

    chunks = chunker.chunk(project_event)

    assert len(chunks) == 1
    assert chunks[0].content == project_event.content


def test_chunker_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="chunk_size"):
        FixedSizeChunker(chunk_size=0)

    with pytest.raises(ValueError, match="overlap"):
        FixedSizeChunker(chunk_size=10, overlap=10)

    with pytest.raises(ValueError, match="overlap"):
        FixedSizeChunker(chunk_size=10, overlap=-1)