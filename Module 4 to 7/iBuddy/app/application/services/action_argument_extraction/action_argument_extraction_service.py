from typing import cast

from app.application.services.action_argument_extraction.models import (
    ApplyLeaveArguments,
    ActionArgumentExtractionRequest,
)
from app.application.services.action_argument_extraction.action_argument_prompt_builder import (
    ActionArgumentPromptBuilder,
)
from app.domain.services.llm_client import (
    LLMClient,
)


class ActionArgumentExtractionService:
    """
    Extracts structured leave request arguments from a natural language request.
    """

    def __init__(
        self,
        llm_client: LLMClient,
        prompt_builder: ActionArgumentPromptBuilder,
    ) -> None:
        self._llm_client = llm_client
        self._prompt_builder = prompt_builder

    def extract(
        self,
        request: ActionArgumentExtractionRequest,
    ) -> ApplyLeaveArguments:

        llm_request = self._prompt_builder.build(
            request,
        )

        return cast(
            ApplyLeaveArguments,
            self._llm_client.generate_structured(
                llm_request,
            ),
        )

