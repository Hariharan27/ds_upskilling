from pydantic import ValidationError

from app.application.services.conversational_query_expansion.models import ConversationalQueryExpansionRequest, ConversationalQueryExpansionResponse
from app.application.services.conversational_query_expansion.conversational_query_expansion_prompt_builder import ConversationalQueryExpansionPromptBuilder
from app.domain.services.conversational_query_expansion_service import ConversationalQueryExpansionService


from app.domain.services.llm_client import (
    LLMClient,
)
from app.shared.exceptions.llm import LLMClientError, LLMResponseError


class LlmConversationalQueryExpansionService(
    ConversationalQueryExpansionService,
):

    def __init__(
        self,
        llm_client: LLMClient,
    ) -> None:

        self._llm_client = llm_client

    def expand(
            self,
            request: ConversationalQueryExpansionRequest,
    ) -> list[str]:

        llm_request = (
            ConversationalQueryExpansionPromptBuilder.build(
                request,
            )
        )

        try:

            llm_response = (
                self._llm_client.generate_text(
                    llm_request,
                )
            )

            expanded_response = (
                ConversationalQueryExpansionResponse.model_validate_json(
                    llm_response.content,
                )
            )

            return list(dict.fromkeys([request.query, *expanded_response.queries]))

        except (
                LLMClientError,
                LLMResponseError,
                ValidationError,
        ) as e:
            print(e)
            return [
                request.query,
            ]