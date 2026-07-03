from abc import ABC, abstractmethod

from app.domain.entities.search_result import SearchResult


class RerankingService(ABC):

    @abstractmethod
    def rerank(
            self,
            query: str,
            results: list[SearchResult],
            top_k: int,
    ) -> list[SearchResult]:
        """
        Rerank retrieved search results.
        """
        raise NotImplementedError