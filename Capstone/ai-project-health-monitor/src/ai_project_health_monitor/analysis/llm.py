from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Contract for interacting with a large language model."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the language model."""
        raise NotImplementedError