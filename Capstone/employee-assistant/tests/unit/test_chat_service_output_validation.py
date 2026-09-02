from unittest.mock import patch

import pytest
from app.core.exceptions import OutputValidationError
from app.services.chat_service import ChatService


def test_invalid_output_is_rejected() -> None:
    service = ChatService()

    with patch(
        "app.services.chat_service.employee_assistant_graph.invoke",
        return_value={
            "response": "",
            "sources": [],
        },
    ):
        with pytest.raises(OutputValidationError):
            service.chat("What is the leave policy?")