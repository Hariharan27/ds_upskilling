from app.ai.graphs.employee_assistant import employee_assistant_graph
from app.core.langfuse import get_langfuse
from app.schemas.chat import ChatResponse


class ChatService:

    def chat(self, message: str) -> ChatResponse:

        langfuse = get_langfuse()

        with langfuse.start_as_current_observation(
            name="employee-assistant",
            as_type="chain",
            input={
                "message": message,
            },
        ) as observation:

            result = employee_assistant_graph.invoke(
                {
                    "message": message,
                }
            )

            observation.update(
                output={
                    "answer": result.get("response", ""),
                    "sources": [
                        {
                            "document": source.document,
                            "page": source.page,
                        }
                        for source in result.get("sources", [])
                    ],
                }
            )

        return ChatResponse(
            answer=result.get("response", ""),
            sources=result.get("sources", []),
        )