from ai_project_health_monitor.rag.embeddings.base import EmbeddingModel
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult
from ai_project_health_monitor.rag.vector_store.base import VectorStore


class RetrievalService:
    """Application service responsible for semantic retrieval."""

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_model = embedding_model
        self._vector_store = vector_store

    def retrieve(
        self,
        query: str,
        project_id: str,
        limit: int = 5,
    ) -> list[RetrievalResult]:
        """Retrieve the most relevant chunks for a project query."""
        if not query.strip():
            raise ValueError("query cannot be empty")

        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        query_embedding = self._embedding_model.embed([query])

        if len(query_embedding) != 1:
            raise ValueError(
                "embedding model must return exactly one vector for the query"
            )

        return self._vector_store.search(
            query_embedding=query_embedding[0],
            project_id=project_id,
            limit=limit,
        )