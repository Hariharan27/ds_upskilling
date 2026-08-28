from typing import Protocol


class Evaluator(Protocol):
    """Interface for response evaluators."""

    def evaluate(self, prompt: str, response: str) -> dict:
        ...


class BasicEvaluator:
    """Deterministic evaluator for basic response quality."""

    def evaluate(self, prompt: str, response: str) -> dict:
        text = response.strip()

        if not text:
            return {
                "score": 0.0,
                "label": "empty",
            }

        if len(text) < 20:
            return {
                "score": 0.5,
                "label": "too_short",
            }

        return {
            "score": 1.0,
            "label": "acceptable",
        }