from sentence_transformers import SentenceTransformer

from app.domain.services.embedding_service import (
    EmbeddingService,
)
from app.shared.config import get_settings

class SentenceTransformerEmbeddingService(
    EmbeddingService
):
    """
    Sentence Transformer implementation
    of EmbeddingService.
    """

    def __init__(
            self,
            model_name: str|None = None,
    ) -> None:

        settings = get_settings()
        self._model = SentenceTransformer(
            model_name or settings.embedding_model
        )

    def embed_text(
            self,
            text: str,
    ) -> list[float]:
        """
        Generate embedding for a single text.
        """

        embedding = self._model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()


    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        embeddings = self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
