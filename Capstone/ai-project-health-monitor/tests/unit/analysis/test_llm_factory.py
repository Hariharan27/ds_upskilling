
import pytest

from ai_project_health_monitor.analysis.llm import LLMClient
from ai_project_health_monitor.analysis.llm_factory import LLMClientFactory
from ai_project_health_monitor.analysis.ollama import OllamaLLMClient
from ai_project_health_monitor.analysis.together import TogetherLLMClient
from ai_project_health_monitor.core.config import LLMProvider, Settings


def test_factory_creates_ollama_client() -> None:
    settings = Settings(
        llm_provider=LLMProvider.OLLAMA,
        llm_model="qwen3:8b",
        ollama_host="http://localhost:11434",
    )

    client = LLMClientFactory.create(settings)

    assert isinstance(client, OllamaLLMClient)


def test_factory_creates_together_client() -> None:
    settings = Settings(
        llm_provider=LLMProvider.TOGETHER,
        llm_model="openai/gpt-oss-20b",
        together_api_key="test-key",
    )

    client = LLMClientFactory.create(settings)

    assert isinstance(client, TogetherLLMClient)


def test_factory_returns_llm_client() -> None:
    settings = Settings(
        llm_provider=LLMProvider.OLLAMA,
        llm_model="qwen3:8b",
    )

    client = LLMClientFactory.create(settings)

    assert isinstance(client, LLMClient)


def test_factory_requires_together_api_key() -> None:
    settings = Settings(
        llm_provider=LLMProvider.TOGETHER,
        llm_model="openai/gpt-oss-20b",
        together_api_key=None,
    )

    with pytest.raises(
        ValueError,
        match="TOGETHER_API_KEY is required",
    ):
        LLMClientFactory.create(settings)


def test_factory_rejects_unimplemented_openai() -> None:
    settings = Settings(
        llm_provider=LLMProvider.OPENAI,
        llm_model="test-model",
    )

    with pytest.raises(
        NotImplementedError,
        match="OpenAI LLM client is not implemented yet",
    ):
        LLMClientFactory.create(settings)