from unittest.mock import patch

from app.services.chat_service import ChatService


def test_chat_service_redacts_pii_from_langfuse_trace() -> None:
    service = ChatService()

    mock_langfuse = patch(
        "app.services.chat_service.get_langfuse"
    ).start()

    mock_graph = patch(
        "app.services.chat_service.employee_assistant_graph.invoke"
    ).start()

    try:
        mock_graph.return_value = {
            "response": "Your request is associated with employee@example.com.",
            "sources": [],
        }

        observation = mock_langfuse.return_value.start_as_current_observation.return_value.__enter__.return_value

        service.chat("Contact me at employee@example.com")

        call = observation.update.call_args

        assert call is not None

        output = call.kwargs["output"]

        assert "employee@example.com" not in output["answer"]
        assert "[REDACTED_EMAIL]" in output["answer"]

        trace_input = (
            mock_langfuse.return_value
            .start_as_current_observation.call_args.kwargs["input"]
        )

        assert "employee@example.com" not in trace_input["message"]
        assert "[REDACTED_EMAIL]" in trace_input["message"]

    finally:
        mock_langfuse.stop()
        mock_graph.stop()