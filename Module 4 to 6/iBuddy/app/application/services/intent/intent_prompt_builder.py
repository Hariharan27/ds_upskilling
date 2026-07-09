from app.domain.models.intent_classification_request import IntentClassificationRequest
from app.domain.models.chat_message import ChatMessage, MessageRole
from app.domain.models.llm_request import LLMRequest
from app.application.services.intent.prompts import SYSTEM_PROMPT
from app.domain.tools.tool_registry import ToolRegistry

class IntentPromptBuilder:

    def __init__(self, tool_registry: ToolRegistry):
        self._tool_registry = tool_registry

    def build(self,
              request: IntentClassificationRequest,) -> LLMRequest:

        available_tools = self._build_available_tools()

        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content= (
                    f"{SYSTEM_PROMPT.strip()}\n\n"
                    "Available Tools\n"
                    "===============\n\n"
                    f"{available_tools}"
                ),
            ),
            *request.conversation_history,
            ChatMessage(
                role=MessageRole.USER,
                content=request.query,
            ),
        ]

        return LLMRequest(
            messages,
            temperature=0.0,
        )

    def _build_available_tools(
            self,
    ) -> str:
        tools = []

        for definition in self._tool_registry.get_tool_definitions():
            tools.append(
                f"""
    Tool Name:
    {definition.name}

    Description:
    {definition.description}
    """.strip()
            )

        return "\n\n".join(
            tools,
        )




