from app.application.services.rag.models import RAGPromptRequest
from app.application.services.rag.prompts import (
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_V2
)

from app.domain.models.llm_request import (
    LLMRequest,
)


class PromptBuilder:

    def build(
        self,
        request: RAGPromptRequest,
    ) -> LLMRequest:

        return LLMRequest(
            system_prompt= SYSTEM_PROMPT_V2,
            user_prompt=self._build_user_prompt(
                query= request.query,
                context= request.context,
            ),
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