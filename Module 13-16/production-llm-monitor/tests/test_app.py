import pytest

from production_llm_monitor.app import LLMApplication
from production_llm_monitor.evaluation import BasicEvaluator
from production_llm_monitor.guardrails import GuardrailViolation, InputGuardrail, OutputGuardrail

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
    app.input_guardrail = InputGuardrail()
    app.output_guardrail = OutputGuardrail()

    response = app.ask("What is RAG?")

    assert response == "Fake response for: What is RAG?"


def test_application_reraises_llm_error():
    app = LLMApplication.__new__(LLMApplication)
    app.llm = FailingLLMClient()
    app.evaluator = BasicEvaluator()
    app.input_guardrail = InputGuardrail()
    app.output_guardrail = OutputGuardrail()

    with pytest.raises(TimeoutError):
        app.ask("What is RAG?")


class EmptyResponseLLMClient:
    model = "openai/gpt-oss-20b"

    def generate(self, prompt: str) -> dict:
        return {
            "content": "",
            "prompt_tokens": 5,
            "completion_tokens": 0,
            "total_tokens": 5,
            "cache_hit": False,
        }

def test_application_blocks_empty_llm_response():
    app = LLMApplication.__new__(LLMApplication)
    app.llm = EmptyResponseLLMClient()
    app.evaluator = BasicEvaluator()
    app.input_guardrail = InputGuardrail()
    app.output_guardrail = OutputGuardrail()

    with pytest.raises(GuardrailViolation):
        app.ask("What is RAG?")

class FailingEvaluator:
    def evaluate(self, prompt: str, response: str) -> dict:
        raise RuntimeError("Evaluation service unavailable")

def test_application_returns_response_when_evaluation_fails():
    app = LLMApplication.__new__(LLMApplication)
    app.llm = FakeLLMClient()
    app.evaluator = FailingEvaluator()
    app.input_guardrail = InputGuardrail()
    app.output_guardrail = OutputGuardrail()

    response = app.ask("What is RAG?")

    assert response == "Fake response for: What is RAG?"

class FakeJudgeEvaluator:
    def evaluate(self, prompt: str, response: str) -> dict:
        return {
            "score": 0.9,
            "label": "good",
            "reason": "Relevant response",
        }

def test_application_runs_llm_and_evaluation_together():
    app = LLMApplication.__new__(LLMApplication)
    app.llm = FakeLLMClient()
    app.evaluator = FakeJudgeEvaluator()
    app.input_guardrail = InputGuardrail()
    app.output_guardrail = OutputGuardrail()

    response = app.ask("What is RAG?")

    assert response == "Fake response for: What is RAG?"