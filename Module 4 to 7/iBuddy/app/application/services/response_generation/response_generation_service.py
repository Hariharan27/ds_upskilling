from app.application.services.response_generation.models import (
    ResponseGenerationRequest,
    ResponseGenerationResponse,
)
from app.application.services.response_generation.response_prompt_builder import (
    ResponsePromptBuilder,
)
from app.domain.services.llm_client import (
    LLMClient,
)


class ResponseGenerationService:

    def __init__(
        self,
        prompt_builder: ResponsePromptBuilder,
        llm_client: LLMClient,
    ) -> None:

        self._prompt_builder = prompt_builder
        self._llm_client = llm_client

    def generate(
        self,
        request: ResponseGenerationRequest,
    ) -> ResponseGenerationResponse:

        llm_request = self._prompt_builder.build(
            request,
        )

        llm_response = self._llm_client.generate_text(
            llm_request,
        )

        return ResponseGenerationResponse(
            answer=llm_response.content,
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
            total_tokens=llm_response.total_tokens,
        )