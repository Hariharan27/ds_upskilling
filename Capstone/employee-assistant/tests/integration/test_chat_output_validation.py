from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_llm_output_returns_controlled_response() -> None:
    with patch(
        "app.services.chat_service.employee_assistant_graph.invoke",
        return_value={
            "response": "",
            "sources": [],
        },
    ):
        response = client.post(
            "/api/v1/chat",
            json={"message": "What is the leave policy?"},
        )

    assert response.status_code == 422
    assert response.json() == {
        "detail": (
            "I couldn't generate a reliable answer for your request. "
            "Please try rephrasing it."
        )
    }