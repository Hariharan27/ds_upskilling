from together import Together

from app.core.config import get_settings


class TogetherLLM:
    """Application-level wrapper around the Together AI client."""

    def __init__(self) -> None:
        settings = get_settings()

        self.client = Together(api_key=settings.together_api_key)
        self.model = settings.together_model

    def generate(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content or ""