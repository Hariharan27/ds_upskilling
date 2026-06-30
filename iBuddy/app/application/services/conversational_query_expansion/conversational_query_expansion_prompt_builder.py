from app.application.services.conversational_query_expansion.models import (
    ConversationalQueryExpansionRequest,
)
from app.application.services.conversational_query_expansion.prompts import (
    SYSTEM_PROMPT,
    OUTPUT_SCHEMA,
)
from app.domain.models.chat_message import ChatMessage, MessageRole

from app.domain.models.llm_request import (
    LLMRequest,
)


class ConversationalQueryExpansionPromptBuilder:
    """
    Builds prompts for query expansion.
    """
    @staticmethod
    def _build_conversation_history(
            conversation_history: list[ChatMessage],
    ) -> str:
        if not conversation_history:
            return "No previous conversation."

        return "\n".join(
            f"{message.role.value}: {message.content}"
            for message in conversation_history
        )

    @staticmethod
    def build(
        request: ConversationalQueryExpansionRequest,
    ) -> LLMRequest:

        conversation_history = ConversationalQueryExpansionPromptBuilder._build_conversation_history(
            request.conversation_history,
        )

        user_prompt = f"""
        Conversation History:

        {conversation_history}

        Current Question:

        {request.query}

        {OUTPUT_SCHEMA}
        """.strip()

        return LLMRequest(
            messages=[
                ChatMessage(
                    role= MessageRole.SYSTEM,
                    content=SYSTEM_PROMPT,
                ),
                ChatMessage(
                    role=MessageRole.USER,
                    content=user_prompt.strip(),
                ),
            ],
        )