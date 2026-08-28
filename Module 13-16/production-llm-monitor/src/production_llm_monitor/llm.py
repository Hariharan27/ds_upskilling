import os

from together import Together
from langfuse import get_client, observe
from production_llm_monitor.cache import InMemoryCache

class LLMClient:
    """Simple Together AI client."""

    def __init__(
        self,
        model: str = "openai/gpt-oss-20b",
        cache: InMemoryCache | None = None,
    ):
        api_key = os.getenv("TOGETHER_API_KEY")

        if not api_key:
            raise ValueError(
                "TOGETHER_API_KEY environment variable is not set."
            )

        self.client = Together(api_key=api_key)
        self.model = model
        self.cache = cache or InMemoryCache()

    @observe(as_type="generation")
    def generate(self, prompt: str) -> dict:
        """Generate a response and return usage information."""

        langfuse = get_client()

        try:

            cached_response = self.cache.get(prompt, self.model)

            if cached_response is not None:
                return {
                    "content": cached_response,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "cache_hit": True,
                }

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            content = response.choices[0].message.content

            self.cache.set(
                prompt,
                self.model,
                content,
            )

            langfuse.update_current_generation(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                output=response.choices[0].message.content,
                usage_details={
                    "input": response.usage.prompt_tokens,
                    "output": response.usage.completion_tokens,
                    "total": response.usage.total_tokens,
                },
            )

            return {
                "content": response.choices[0].message.content,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "cache_hit": False,
            }

        except Exception as exc:
            langfuse.update_current_generation(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                status_message=str(exc),
                level="ERROR",
            )
            raise