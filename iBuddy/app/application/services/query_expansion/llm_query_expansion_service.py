from pydantic import ValidationError

from app.application.services.query_expansion.models import QueryExpansionRequest, QueryExpansionResponse
from app.application.services.query_expansion.prompt_builder import QueryExpansionPromptBuilder
from app.domain.services.query_expansion_service import QueryExpansionService


from app.domain.services.llm_client import (
    LLMClient,
)
from app.shared.exceptions.llm import LLMClientError, LLMResponseError


class LlmQueryExpansionService(
    QueryExpansionService,
):

    def __init__(
        self,
        llm_client: LLMClient,
    ) -> None:

        self._llm_client = llm_client

    def expand(
            self,
            query: str,
    ) -> list[str]:

        request = QueryExpansionRequest(
            query=query,
        )

        llm_request = (
            QueryExpansionPromptBuilder.build(
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
                QueryExpansionResponse.model_validate_json(
                    llm_response.content,
                )
            )

            return list(dict.fromkeys([query, *expanded_response.queries]))

        except (
                LLMClientError,
                LLMResponseError,
                ValidationError,
        ) as e:
            print(e)
            return [
                query,
            ]