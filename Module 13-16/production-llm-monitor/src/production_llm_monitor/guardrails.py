import re


class GuardrailViolation(Exception):
    """Raised when a request or response violates a guardrail."""


class InputGuardrail:
    """Basic input safety checks."""

    def validate(self, prompt: str) -> None:
        if not prompt.strip():
            raise GuardrailViolation("Prompt cannot be empty.")

        suspicious_patterns = [
            r"ignore\s+(all\s+)?previous\s+instructions",
            r"system\s+prompt",
            r"reveal\s+(your\s+)?instructions",
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                raise GuardrailViolation(
                    "Prompt contains a potentially unsafe instruction."
                )


class OutputGuardrail:
    """Basic output safety checks."""

    def validate(self, response: str) -> None:
        if not response.strip():
            raise GuardrailViolation("Model returned an empty response.")