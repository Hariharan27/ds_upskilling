import re


PROMPT_INJECTION_PATTERNS = (
    r"\bignore (all |any |the )?(previous|prior|above) instructions\b",
    r"\bdisregard (all |any |the )?(previous|prior|above) instructions\b",
    r"\bforget (all |any |the )?(previous|prior|above) instructions\b",
    r"\breveal (the )?(system|developer) prompt\b",
    r"\bshow (me )?(the )?(system|developer) prompt\b",
    r"\breveal (the )?(hidden|secret) instructions\b",
    r"\bbypass (your )?(rules|instructions|restrictions)\b",
    r"\byou are now (an? )?(admin|administrator)\b",
    r"\b(tell me|show me|give me|provide) (your )?(hidden|secret) instructions\b",
)


def is_prompt_injection(message: str) -> bool:
    """Return True when a message matches a high-confidence injection pattern."""

    normalized_message = " ".join(message.lower().split())

    return any(
        re.search(pattern, normalized_message)
        for pattern in PROMPT_INJECTION_PATTERNS
    )