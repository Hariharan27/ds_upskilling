from app.application.services.query_expansion.models import (
    QueryExpansionRequest,
)
from app.application.services.query_expansion.prompts import (
    SYSTEM_PROMPT,
    OUTPUT_SCHEMA,
)
from app.domain.models.chat_message import ChatMessage, MessageRole

from app.domain.models.llm_request import (
    LLMRequest,
)


class QueryExpansionPromptBuilder:
    """
    Builds prompts for query expansion.
    """

    @staticmethod
    def build(
        request: QueryExpansionRequest,
    ) -> LLMRequest:

        user_prompt = f"""
                        User Query:
                            
                        {request.query}
                            
                        {OUTPUT_SCHEMA}
                        
                        """

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