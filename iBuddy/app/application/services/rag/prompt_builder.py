from app.application.services.rag.models import RAGPromptRequest
from app.application.services.rag.prompts import (
    SYSTEM_PROMPT_V2
)
from app.domain.models.chat_message import ChatMessage, MessageRole

from app.domain.models.llm_request import (
    LLMRequest,
)


class PromptBuilder:

    def build(
        self,
        request: RAGPromptRequest,
    ) -> LLMRequest:

        messages: list[ChatMessage] = [
            ChatMessage(
                role= MessageRole.SYSTEM,
                content=SYSTEM_PROMPT_V2,
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
        Build the user prompt for RAG.
        """

        return f"""
    {context}

    Question:

    {query}
    
    """.strip()