from pathlib import Path

from ai_project_health_monitor.ingestion.connectors.synthetic_document import (
    SyntheticDocumentConnector,
)


def test_synthetic_document_connector_returns_project_events(
    tmp_path: Path,
) -> None:
    document = tmp_path / "status.md"
    document.write_text(
        "# Project Status\n\nThe project is delayed.",
        encoding="utf-8",
    )

    connector = SyntheticDocumentConnector(tmp_path)

    events = connector.fetch_events("PROJ-001")

    assert len(events) == 1
    assert events[0].project_id == "PROJ-001"
    assert events[0].source_type.value == "document"
    assert events[0].source_id == "status.md"
    assert "project is delayed" in events[0].content
    assert events[0].metadata["file_type"] == "markdown"


def test_synthetic_document_connector_ignores_empty_documents(
    tmp_path: Path,
) -> None:
    empty_document = tmp_path / "empty.md"
    empty_document.write_text("   ", encoding="utf-8")

    connector = SyntheticDocumentConnector(tmp_path)

    events = connector.fetch_events("PROJ-001")

    assert events == []


def test_synthetic_document_connector_ignores_non_markdown_files(
    tmp_path: Path,
) -> None:
    markdown = tmp_path / "status.md"
    markdown.write_text("Project update.", encoding="utf-8")

    text_file = tmp_path / "notes.txt"
    text_file.write_text("Should be ignored.", encoding="utf-8")

    connector = SyntheticDocumentConnector(tmp_path)

    events = connector.fetch_events("PROJ-001")

    assert len(events) == 1
    assert events[0].source_id == "status.md"