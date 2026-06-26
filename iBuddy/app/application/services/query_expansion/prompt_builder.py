from app.application.services.query_expansion.models import (
    QueryExpansionRequest,
)
from app.application.services.query_expansion.prompts import (
    SYSTEM_PROMPT,
    OUTPUT_SCHEMA,
)
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
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt.strip(),
        )