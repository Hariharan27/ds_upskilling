import os

from together import Together


class LLMClient:
    """Client responsible for communicating with Together AI."""

    def __init__(
        self,
        model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    ):
        api_key = os.getenv("TOGETHER_API_KEY")

        if not api_key:
            raise ValueError(
                "TOGETHER_API_KEY environment variable is not set."
            )

        self.client = Together(api_key=api_key)
        self.model = model

    def generate_response(
        self,
        message: str,
    ) -> str:
        """Send a message to Together AI and return the response."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )

        return response.choices[0].message.content

    def generate_stream(
        self,
        message: str,
    ):
        """Stream the LLM response chunk by chunk."""

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                yield content