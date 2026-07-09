from fastapi import Depends

from app.application.services.response_generation.response_generation_service import (
    ResponseGenerationService,
)
from app.application.services.response_generation.response_prompt_builder import (
    ResponsePromptBuilder,
)
from app.domain.services.llm_client import (
    LLMClient,
)
from app.presentation.api.dependencies.llm import (
    get_client,
)


def get_response_generation_service(
    llm_client: LLMClient = Depends(
        get_client,
    ),
) -> ResponseGenerationService:

    prompt_builder = ResponsePromptBuilder()

    return ResponseGenerationService(
        prompt_builder=prompt_builder,
        llm_client=llm_client,
    )