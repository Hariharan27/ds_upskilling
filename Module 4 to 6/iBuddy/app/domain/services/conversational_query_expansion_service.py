from abc import ABC, abstractmethod

from app.application.services.conversational_query_expansion.models import ConversationalQueryExpansionRequest


class ConversationalQueryExpansionService(ABC):

    @abstractmethod
    def expand(self,request: ConversationalQueryExpansionRequest) -> list[str]:
        """
        Generate alternative search queries.
        """
        raise NotImplementedError