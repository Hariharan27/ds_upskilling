from pydantic import ValidationError

from app.ai.guardrails.input import is_prompt_injection
from app.ai.graphs.employee_assistant import employee_assistant_graph
from app.core.langfuse import get_langfuse
from app.schemas.chat import ChatResponse
from app.ai.guardrails.pii import redact_pii
from app.core.exceptions import OutputValidationError
from app.ai.guardrails.output import contains_unsafe_output

class ChatService:

    def chat(self, message: str) -> ChatResponse:

        if is_prompt_injection(message):
            return ChatResponse(
                answer=(
                    "I can help with employee policies and HR-related requests, "
                    "but I can't follow requests to override my instructions."
                ),
                sources=[],
            )

        langfuse = get_langfuse()

        with langfuse.start_as_current_observation(
            name="employee-assistant",
            as_type="chain",
            input={"message": redact_pii(message)},
        ) as observation:

            result = employee_assistant_graph.invoke(
                {
                    "message": message,
                }
            )

            answer = result.get("response", "")

            if contains_unsafe_output(answer):
                raise OutputValidationError(
                    "The generated response failed output safety validation."
                )

            observation.update(
                output={
                    "answer": redact_pii(result.get("response", "")),
                    "sources": [
                        {
                            "document": redact_pii(source.document),
                            "page": source.page,
                        }
                        for source in result.get("sources", [])
                    ],
                }
            )

        try:
            return ChatResponse(
                answer=result.get("response", ""),
                sources=result.get("sources", []),
            )
        except ValidationError as exc:
            raise OutputValidationError(
                "The generated response failed output validation."
            ) from exc