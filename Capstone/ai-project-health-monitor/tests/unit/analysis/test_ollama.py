from unittest.mock import Mock

import pytest

from ai_project_health_monitor.analysis.ollama import OllamaLLMClient


def test_generate_returns_model_content() -> None:
    mock_client = Mock()
    mock_client.chat.return_value = {
        "message": {
            "content": "The project has a delivery risk.",
        }
    }

    client = OllamaLLMClient(model="qwen3:8b")
    client._client = mock_client

    result = client.generate("Analyze this project.")

    assert result == "The project has a delivery risk."

    mock_client.chat.assert_called_once_with(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": "Analyze this project.",
            }
        ],
    )


def test_generate_rejects_empty_prompt() -> None:
    client = OllamaLLMClient(model="qwen3:8b")

    with pytest.raises(ValueError, match="prompt cannot be empty"):
        client.generate("   ")


def test_constructor_rejects_empty_model() -> None:
    with pytest.raises(ValueError, match="model cannot be empty"):
        OllamaLLMClient(model="   ")


def test_constructor_rejects_empty_host() -> None:
    with pytest.raises(ValueError, match="host cannot be empty"):
        OllamaLLMClient(
            model="qwen3:8b",
            host="   ",
        )


def test_generate_rejects_non_string_content() -> None:
    mock_client = Mock()
    mock_client.chat.return_value = {
        "message": {
            "content": 123,
        }
    }

    client = OllamaLLMClient(model="qwen3:8b")
    client._client = mock_client

    with pytest.raises(
        TypeError,
        match="Ollama response content must be a string",
    ):
        client.generate("Analyze this project.")