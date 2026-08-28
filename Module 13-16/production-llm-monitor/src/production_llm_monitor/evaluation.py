import json
import os

from typing import Protocol
from together import Together

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

class LLMJudgeEvaluator:
    """LLM-based evaluator for response quality."""

    def __init__(
        self,
        model: str = "openai/gpt-oss-20b",
    ):
        api_key = os.getenv("TOGETHER_API_KEY")

        if not api_key:
            raise ValueError(
                "TOGETHER_API_KEY environment variable is not set."
            )

        self.client = Together(api_key=api_key)
        self.model = model

    def evaluate(self, prompt: str, response: str) -> dict:
        """Evaluate an LLM response using a judge model."""

        judge_prompt = f"""
You are an evaluator for an LLM application.

Evaluate the response against the user's prompt.

User prompt:
{prompt}

Assistant response:
{response}

Return ONLY valid JSON with exactly these fields:
{{
    "score": <number between 0 and 1>,
    "label": "<good, acceptable, or poor>",
    "reason": "<brief explanation>"
}}

Scoring:
- 1.0 = correct, relevant, and well-written
- 0.5 = partially correct or has minor issues
- 0.0 = incorrect, irrelevant, or unusable
"""

        result = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": judge_prompt,
                }
            ],
        )

        content = result.choices[0].message.content

        evaluation = json.loads(content)

        return {
            "score": float(evaluation["score"]),
            "label": evaluation["label"],
            "reason": evaluation["reason"],
        }