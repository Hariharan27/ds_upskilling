from app.application.services.response_generation.models import ResponseGenerationRequest
from app.application.services.response_generation.prompts import (
    SYSTEM_PROMPT
)
from app.domain.models.chat_message import ChatMessage, MessageRole

from app.domain.models.llm_request import (
    LLMRequest,
)


class ResponsePromptBuilder:

    def build(
            self,
            request: ResponseGenerationRequest,
    ) -> LLMRequest:
        messages: list[ChatMessage] = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=SYSTEM_PROMPT,
            )
        ]

        messages.extend(
            request.conversation_history,
        )

        messages.append(
            ChatMessage(
                role=MessageRole.USER,
                content=self._build_user_prompt(
                    query=request.query,
                    context=request.context,
                ),
            )
        )

        return LLMRequest(
            messages=messages,
        )

    def _build_user_prompt(
            self,
            query: str,
            context: str,
    ) -> str:
        """
        Build the user prompt for response generation.
        """

        return f"""
        Context:
        {context}

        User Question:
        {query}
        """.strip()