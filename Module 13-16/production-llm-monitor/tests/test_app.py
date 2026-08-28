import pytest

from production_llm_monitor.app import LLMApplication
from production_llm_monitor.evaluation import BasicEvaluator

class FakeLLMClient:
    model = "openai/gpt-oss-20b"

    def generate(self, prompt: str) -> dict:
        return {
            "content": f"Fake response for: {prompt}",
            "prompt_tokens": 5,
            "completion_tokens": 7,
            "total_tokens": 12,
            "cache_hit": False,
        }


class FailingLLMClient:
    model = "openai/gpt-oss-20b"

    def generate(self, prompt: str) -> dict:
        raise TimeoutError("LLM request timed out")


def test_application_returns_llm_response():
    app = LLMApplication.__new__(LLMApplication)
    app.llm = FakeLLMClient()
    app.evaluator = BasicEvaluator()

    response = app.ask("What is RAG?")

    assert response == "Fake response for: What is RAG?"


def test_application_reraises_llm_error():
    app = LLMApplication.__new__(LLMApplication)
    app.llm = FailingLLMClient()

    with pytest.raises(TimeoutError):
        app.ask("What is RAG?")