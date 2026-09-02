import re


PII_PATTERNS = {
    "email": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "phone": re.compile(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"
    ),
    "aadhaar": re.compile(
        r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"
    ),
    "pan": re.compile(
        r"\b[A-Z]{5}\d{4}[A-Z]\b"
    ),
}


def redact_pii(text: str) -> str:
    """Redact common PII before sending text to logs or observability."""

    redacted = text

    for pii_type, pattern in PII_PATTERNS.items():
        redacted = pattern.sub(
            f"[REDACTED_{pii_type.upper()}]",
            redacted,
        )

    return redacted