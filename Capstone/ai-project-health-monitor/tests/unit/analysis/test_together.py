from unittest.mock import Mock

from ai_project_health_monitor.analysis.together import TogetherLLMClient


def test_together_client_passes_generation_controls() -> None:
    mock_client = Mock()
    mock_client.chat.completions.create.return_value.choices = [
        Mock(message=Mock(content='{"ok": true}'))
    ]

    client = TogetherLLMClient(
        model="openai/gpt-oss-20b",
        api_key="test-key",
    )
    client._client = mock_client

    result = client.generate("test prompt")

    assert result == '{"ok": true}'

    request = mock_client.chat.completions.create.call_args.kwargs

    assert request["max_tokens"] == 2048
    assert request["reasoning_effort"] == "low"


def test_together_client_rejects_invalid_reasoning_effort() -> None:
    try:
        TogetherLLMClient(
            model="openai/gpt-oss-20b",
            api_key="test-key",
            reasoning_effort="invalid",
        )
    except ValueError as exc:
        assert "reasoning_effort must be one of" in str(exc)
    else:
        raise AssertionError("Expected ValueError")