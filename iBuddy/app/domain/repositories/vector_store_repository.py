from abc import ABC, abstractmethod

from app.domain.entities.chunk import Chunk
from app.domain.entities.search_result import SearchResult


class VectorStoreRepository(ABC):
    """
    Contract for vector storage
    and similarity search.
    """

    @abstractmethod
    def add_chunks(self,
                   chunks: list[Chunk],
                   embeddings: list[list[float]]
                   ) -> None:
        """
        Store chunks and embeddings.
        """
        raise NotImplementedError


    @abstractmethod
    def search(self,
               query_embeddings: list[float],
               top_k: int  = 5,
                metadata_filter: dict[str, str] | None = None,
               ) -> list[SearchResult]:
        """
        Perform similarity search.
        """
        raise NotImplementedError


    @abstractmethod
    def delete_by_document_id(
            self,
            document_id: str
    ) -> None:
            """
            Delete all chunks belonging
            to a document.
            """
            raise NotImplementedError

