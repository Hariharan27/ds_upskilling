from abc import ABC, abstractmethod

class EmbeddingService(ABC):
    """
    Contract for generating embeddings.
    """
    @abstractmethod
    def embed_text(
            self,
            text: str
    ) -> list[float]:
        """
        Generate embedding for a single text.
        """
        raise NotImplementedError
    

    @abstractmethod
    def embed_texts(
            self,
            texts: list[str]
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        raise NotImplementedError