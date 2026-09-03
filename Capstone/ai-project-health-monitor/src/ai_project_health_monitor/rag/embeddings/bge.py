from sentence_transformers import SentenceTransformer

from ai_project_health_monitor.rag.embeddings.base import EmbeddingModel


class BGEEmbeddingModel(EmbeddingModel):
    """Generate embeddings using BAAI/bge-small-en-v1.5."""

    MODEL_NAME = "BAAI/bge-small-en-v1.5"

    def __init__(self) -> None:
        self._model = SentenceTransformer(self.MODEL_NAME)

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self._model.encode(
            texts,
            normalize_embeddings=True,
        )

        return [
            [float(value) for value in embedding]
            for embedding in embeddings
        ]