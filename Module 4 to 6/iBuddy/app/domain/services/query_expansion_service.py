from abc import ABC, abstractmethod

class QueryExpansionService(ABC):

    @abstractmethod
    def expand(self,query: str) -> list[str]:
        """
        Generate alternative search queries.
        """
        raise NotImplementedError