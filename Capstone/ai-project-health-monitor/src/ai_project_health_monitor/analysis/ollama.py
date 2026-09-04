from ollama import Client

from ai_project_health_monitor.analysis.llm import LLMClient


class OllamaLLMClient(LLMClient):
    """LLM client implementation backed by a local Ollama server."""

    def __init__(
        self,
        model: str,
        host: str = "http://localhost:11434",
    ) -> None:
        if not model.strip():
            raise ValueError("model cannot be empty")

        if not host.strip():
            raise ValueError("host cannot be empty")

        self._model = model
        self._client = Client(host=host)

    def generate(self, prompt: str) -> str:
        """Generate a response using the configured Ollama model."""
        if not prompt.strip():
            raise ValueError("prompt cannot be empty")

        response = self._client.chat(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response["message"]["content"]

        if not isinstance(content, str):
            raise TypeError("Ollama response content must be a string")

        return content