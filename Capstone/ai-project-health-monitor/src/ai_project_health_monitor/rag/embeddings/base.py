from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    """Contract for converting text into embedding vectors."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate one embedding vector for each text."""
        raise NotImplementedError