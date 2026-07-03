from abc import ABC, abstractmethod

from app.domain.models.llm_request import LLMRequest
from app.domain.models.llm_response import LLMResponse


class LLMClient(ABC):

    @abstractmethod
    def generate_text(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate text from the LLM.
        """
        raise NotImplementedError