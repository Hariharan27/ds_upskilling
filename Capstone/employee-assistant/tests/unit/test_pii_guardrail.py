from app.ai.guardrails.pii import redact_pii


def test_redacts_email() -> None:
    text = "Contact me at employee@example.com."

    result = redact_pii(text)

    assert "employee@example.com" not in result
    assert "[REDACTED_EMAIL]" in result


def test_redacts_phone_number() -> None:
    text = "My phone number is 9876543210."

    result = redact_pii(text)

    assert "9876543210" not in result
    assert "[REDACTED_PHONE]" in result


def test_redacts_aadhaar_number() -> None:
    text = "My Aadhaar number is 1234 5678 9012."

    result = redact_pii(text)

    assert "1234 5678 9012" not in result
    assert "[REDACTED_AADHAAR]" in result


def test_redacts_pan() -> None:
    text = "My PAN is ABCDE1234F."

    result = redact_pii(text)

    assert "ABCDE1234F" not in result
    assert "[REDACTED_PAN]" in result


def test_preserves_normal_hr_text() -> None:
    text = "How many leave days can I take?"

    result = redact_pii(text)

    assert result == text