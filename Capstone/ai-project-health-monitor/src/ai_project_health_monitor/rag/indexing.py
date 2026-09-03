from ai_project_health_monitor.domain.models.project_event import ProjectEvent
from ai_project_health_monitor.rag.chunking import Chunker
from ai_project_health_monitor.rag.embeddings.base import EmbeddingModel
from ai_project_health_monitor.rag.vector_store.base import VectorStore


class RAGIndexer:
    """Index project events into the configured vector store."""

    def __init__(
        self,
        chunker: Chunker,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
    ) -> None:
        self._chunker = chunker
        self._embedding_model = embedding_model
        self._vector_store = vector_store

    def index(self, events: list[ProjectEvent]) -> int:
        """Chunk, embed, and store project events.

        Returns the number of chunks indexed.
        """
        if not events:
            return 0

        chunks = [
            chunk
            for event in events
            for chunk in self._chunker.chunk(event)
        ]

        if not chunks:
            return 0

        embeddings = self._embedding_model.embed(
            [chunk.content for chunk in chunks]
        )

        if len(embeddings) != len(chunks):
            raise ValueError(
                "embedding model must return one vector per chunk"
            )

        self._vector_store.upsert(
            chunks=chunks,
            embeddings=embeddings,
        )

        return len(chunks)