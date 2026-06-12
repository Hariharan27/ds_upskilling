import json

from app.services.llm.together_client import (
    TogetherClient
)

from app.services.prompts.prompt_builder import (
    build_messages
)

from app.schemas.response import (
    ClassificationApiResponse,
    TicketClassificationResponse
)

from app.services.security.prompt_injection import (
    is_prompt_injection
)

from app.services.llm.exceptions import (
    PromptInjectionError
)

from app.services.cost.cost_calculator import (
    CostCalculator
)

from app.core.logging_config import logger

from app.services.prompts.versions import PromptVersion

from app.services.prompts.prompt_selector import (
    PromptSelector
)



class ClassifierService:

    def __init__(self):
        self.llm_client = TogetherClient()

    def classify(
            self,
            employee_message: str
    ):

        if is_prompt_injection(
                employee_message
        ):
            logger.warning(
                "Potential prompt injection detected"
            )

            raise PromptInjectionError(
                "Potential prompt injection detected"
            )

        selected_version = (
            PromptSelector.select()
        )

        logger.info(
            f"Prompt Version={selected_version}"
        )

        messages = build_messages(employee_message,selected_version)

        response = self.llm_client.generate(
            messages=messages
        )

        response_data = json.loads(
            response.content
        )

        cost = CostCalculator.calculate(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens
            )

        logger.info(
            f"Estimated Cost=${cost.total_cost_usd}"
        )

        classification = TicketClassificationResponse(
                **response_data
            )

        logger.info(
            f"Classification="
            f"{classification.department}"
        )

        classification = ClassificationApiResponse(
            classification = classification,
            usage=response.usage,
            cost=cost,
            prompt_version=selected_version
        )
        return classification