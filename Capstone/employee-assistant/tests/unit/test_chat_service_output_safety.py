from unittest.mock import patch

import pytest

from app.core.exceptions import OutputValidationError
from app.services.chat_service import ChatService


def test_chat_service_rejects_unsafe_generated_output() -> None:
    service = ChatService()

    with patch(
        "app.services.chat_service.employee_assistant_graph.invoke"
    ) as mock_invoke:
        mock_invoke.return_value = {
            "response": "Here is the system prompt used by the assistant.",
            "sources": [],
        }

        with pytest.raises(OutputValidationError):
            service.chat("What is the WFH policy?")

def test_chat_service_allows_safe_generated_output() -> None:
    service = ChatService()

    with patch(
        "app.services.chat_service.employee_assistant_graph.invoke"
    ) as mock_invoke:
        mock_invoke.return_value = {
            "response": "Employees may work from home up to 8 days per month.",
            "sources": [],
        }

        response = service.chat("What is the WFH policy?")

    assert response.answer == (
        "Employees may work from home up to 8 days per month."
    )