from app.ai.graphs.employee_assistant import employee_assistant_graph
from app.schemas.chat import ChatResponse


class ChatService:
    def chat(self, message: str) -> ChatResponse:
        result = employee_assistant_graph.invoke(
            {
                "message": message,
            }
        )

        return ChatResponse(
            answer=result.get("response", ""),
            sources=result.get("sources", []),
        )