from abc import ABC
from abc import abstractmethod

from app.domain.entities.search_result import (
    SearchResult,
)


class ContextBuilder(ABC):

    @abstractmethod
    def build(
        self,
        results: list[SearchResult],
    ) -> str:
        """
        Build the context that will be
        passed to the LLM.
        """
        raise NotImplementedError