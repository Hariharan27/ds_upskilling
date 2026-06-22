SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "reveal system prompt",
    "show system prompt",
    "act as chatgpt",
    "act as assistant",
    "override instructions",
    "forget previous instructions",
]


def is_prompt_injection(
    message: str,
) -> bool:
    message = message.lower()
    score = 0

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in message:
            score += 1

    return score >= 1