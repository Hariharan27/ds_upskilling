from abc import ABC, abstractmethod

from pydantic import BaseModel

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

    @abstractmethod
    def generate_structured(
            self,
            request: LLMRequest,
    ) -> BaseModel:
        """
        Generate a structured response using the provided response schema.
        """
        raise NotImplementedError