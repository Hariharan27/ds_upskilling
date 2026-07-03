from abc import ABC, abstractmethod
from app.domain.entities.document import Document
from app.domain.entities.chunk import Chunk

class ChunkingService(ABC):
    """
    Contract for converting documents
    into chunks.
    """

    @abstractmethod
    def chunk_document(
        self,
        document: Document
    ) -> list[Chunk]:
        """
        Split a document into chunks.
        """
        raise NotImplementedError