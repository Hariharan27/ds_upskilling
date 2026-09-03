from datetime import datetime
from uuid import UUID, uuid5

from qdrant_client import QdrantClient, models

from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.rag.models.chunk import DocumentChunk
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.vector_store.base import VectorStore


class QdrantVectorStore(VectorStore):
    """Qdrant-backed vector store for project document chunks."""

    COLLECTION_NAME = "project_health_chunks"
    QDRANT_ID_NAMESPACE = UUID("8b7d8f4e-6c2a-4d6b-9a4e-1f8d7e5c3b21")

    def __init__(
        self,
        client: QdrantClient,
        vector_size: int,
    ) -> None:
        if vector_size <= 0:
            raise ValueError("vector_size must be greater than zero")

        self._client = client
        self._vector_size = vector_size

        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Create the collection if it does not already exist."""
        collections = self._client.get_collections().collections

        if any(
            collection.name == self.COLLECTION_NAME
            for collection in collections
        ):
            return

        self._client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=self._vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def _to_qdrant_id(self, chunk_id: str) -> str:
        """Convert a domain chunk ID into a deterministic Qdrant UUID."""
        return str(uuid5(self.QDRANT_ID_NAMESPACE, chunk_id))

    def _result_from_qdrant(
        self,
        result: models.ScoredPoint,
    ) -> RetrievalResult:
        payload = result.payload

        if payload is None:
            raise ValueError(
                f"Qdrant result {result.id} has no payload"
            )

        required_fields = {
            "chunk_id",
            "project_id",
            "event_id",
            "source_type",
            "source_id",
            "content",
            "chunk_index",
            "occurred_at",
        }

        missing_fields = required_fields - payload.keys()

        if missing_fields:
            raise ValueError(
                f"Qdrant result {result.id} is missing payload fields: "
                f"{sorted(missing_fields)}"
            )

        chunk = DocumentChunk(
            chunk_id=str(payload["chunk_id"]),
            project_id=str(payload["project_id"]),
            event_id=str(payload["event_id"]),
            source_type=SourceType(str(payload["source_type"])),
            source_id=str(payload["source_id"]),
            content=str(payload["content"]),
            chunk_index=int(payload["chunk_index"]),
            occurred_at=datetime.fromisoformat(
                str(payload["occurred_at"])
            ),
        )

        return RetrievalResult(
            chunk=chunk,
            score=float(result.score),
        )

    def upsert(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        """Store chunks and their embeddings in Qdrant."""
        if len(chunks) != len(embeddings):
            raise ValueError(
                "chunks and embeddings must have the same length"
            )

        points = [
            models.PointStruct(
                id=self._to_qdrant_id(chunk.chunk_id),
                vector=embedding,
                payload={
                    "chunk_id": chunk.chunk_id,
                    "project_id": chunk.project_id,
                    "event_id": chunk.event_id,
                    "source_type": chunk.source_type.value,
                    "source_id": chunk.source_id,
                    "content": chunk.content,
                    "chunk_index": chunk.chunk_index,
                    "occurred_at": chunk.occurred_at.isoformat(),
                },
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
                strict=True,
            )
        ]

        if points:
            self._client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=points,
            )

    def search(
        self,
        query_embedding: list[float],
        project_id: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:
        """Retrieve the most relevant chunks for a project."""
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        response = self._client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_embedding,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="project_id",
                        match=models.MatchValue(value=project_id),
                    )
                ]
            ),
            limit=limit,
        )

        return [
            self._result_from_qdrant(result)
            for result in response.points
        ]