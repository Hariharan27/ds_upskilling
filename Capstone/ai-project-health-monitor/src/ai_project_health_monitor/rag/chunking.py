from abc import ABC, abstractmethod

from ai_project_health_monitor.domain.models.project_event import ProjectEvent
from ai_project_health_monitor.rag.models.chunk import DocumentChunk


class Chunker(ABC):
    """Contract for converting project events into retrievable chunks."""

    @abstractmethod
    def chunk(self, event: ProjectEvent) -> list[DocumentChunk]:
        """Split a project event into retrievable chunks."""
        raise NotImplementedError
    

class FixedSizeChunker(Chunker):
    """Split event content into deterministic character-based chunks."""

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")

        if overlap < 0:
            raise ValueError("overlap cannot be negative")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self._chunk_size = chunk_size
        self._overlap = overlap

    def chunk(self, event: ProjectEvent) -> list[DocumentChunk]:
        content = event.content.strip()

        if not content:
            return []

        chunks: list[DocumentChunk] = []
        start = 0
        chunk_index = 0
        step = self._chunk_size - self._overlap

        while start < len(content):
            end = min(start + self._chunk_size, len(content))

            chunks.append(
                DocumentChunk(
                    chunk_id=f"{event.event_id}-CHUNK-{chunk_index:03d}",
                    project_id=event.project_id,
                    event_id=event.event_id,
                    source_type=event.source_type,
                    source_id=event.source_id,
                    content=content[start:end],
                    chunk_index=chunk_index,
                    occurred_at=event.occurred_at,
                )
            )

            if end == len(content):
                break

            start += step
            chunk_index += 1

        return chunks