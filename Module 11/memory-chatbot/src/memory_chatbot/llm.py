import os

from together import Together

class LLMClient:
    """Handles communication with Together AI."""

    def __init__(self, model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"):
        api_key = os.getenv("TOGETHER_API_KEY")

        if not api_key:
            raise ValueError(
                "TOGETHER_API_KEY environment variable is not set."
            )

        self.client = Together(api_key=api_key)
        self.model = model

    def generate_response(self, messages: list[dict[str, str]]) -> str:
        """Generate a response using Together AI."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content