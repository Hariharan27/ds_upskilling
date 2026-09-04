from ai_project_health_monitor.analysis.llm import LLMClient
from ai_project_health_monitor.analysis.ollama import OllamaLLMClient
from ai_project_health_monitor.analysis.together import TogetherLLMClient
from ai_project_health_monitor.core.config import LLMProvider, Settings


class LLMClientFactory:
    """Create an LLM client from application configuration."""

    @staticmethod
    def create(settings: Settings) -> LLMClient:
        if settings.llm_provider == LLMProvider.OLLAMA:
            return OllamaLLMClient(
                model=settings.llm_model,
                host=settings.ollama_host,
            )

        if settings.llm_provider == LLMProvider.TOGETHER:
            if not settings.together_api_key:
                raise ValueError(
                    "TOGETHER_API_KEY is required when LLM_PROVIDER is together"
                )

            return TogetherLLMClient(
                model=settings.llm_model,
                api_key=settings.together_api_key,
            )

        if settings.llm_provider == LLMProvider.OPENAI:
            raise NotImplementedError(
                "OpenAI LLM client is not implemented yet"
            )

        raise ValueError(
            f"Unsupported LLM provider: {settings.llm_provider}"
        )