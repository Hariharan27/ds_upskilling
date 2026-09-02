import re


UNSAFE_OUTPUT_PATTERNS = (
    r"\b(system prompt|developer prompt)\b",
    r"\b(hidden instructions|secret instructions)\b",
)


def contains_unsafe_output(text: str) -> bool:
    """Return True when generated output contains sensitive instruction content."""

    normalized_text = " ".join(text.lower().split())

    return any(
        re.search(pattern, normalized_text)
        for pattern in UNSAFE_OUTPUT_PATTERNS
    )