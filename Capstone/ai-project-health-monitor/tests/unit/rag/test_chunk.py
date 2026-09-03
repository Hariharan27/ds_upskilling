from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.rag.models.chunk import DocumentChunk


def test_document_chunk_creation() -> None:
    chunk = DocumentChunk(
        chunk_id="CHUNK-001",
        project_id="PROJ-001",
        event_id="EVT-001",
        source_type=SourceType.JIRA,
        source_id="PROJ-101",
        content="Payment API integration is blocked.",
        chunk_index=0,
        occurred_at=datetime(2026, 9, 1, 9, 30, tzinfo=UTC),
    )

    assert chunk.chunk_id == "CHUNK-001"
    assert chunk.project_id == "PROJ-001"
    assert chunk.source_type == SourceType.JIRA
    assert chunk.chunk_index == 0


def test_document_chunk_rejects_empty_content() -> None:
    with pytest.raises(ValidationError):
        DocumentChunk(
            chunk_id="CHUNK-001",
            project_id="PROJ-001",
            event_id="EVT-001",
            source_type=SourceType.JIRA,
            source_id="PROJ-101",
            content="",
            chunk_index=0,
            occurred_at=datetime(2026, 9, 1, 9, 30, tzinfo=UTC),
        )


def test_document_chunk_rejects_negative_chunk_index() -> None:
    with pytest.raises(ValidationError):
        DocumentChunk(
            chunk_id="CHUNK-001",
            project_id="PROJ-001",
            event_id="EVT-001",
            source_type=SourceType.JIRA,
            source_id="PROJ-101",
            content="Payment API integration is blocked.",
            chunk_index=-1,
            occurred_at=datetime(2026, 9, 1, 9, 30, tzinfo=UTC),
        )