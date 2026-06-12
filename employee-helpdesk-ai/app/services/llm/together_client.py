import time

from together import Together
from app.core.config import settings
from app.schemas.response import UsageResponse
from app.services.llm.models import (
    LLMResponse
)
from  app.services.llm.exceptions import (
LLMServiceError,
LLMResponseError
)
from together.types.chat import completion_create_params

from app.core.logging_config import logger



class TogetherClient:

    def __init__(self):
        self.client = Together(
            api_key=settings.TOGETHER_API_KEY
        )

    def generate(
            self,
            messages: list[completion_create_params.Message]
    ) -> LLMResponse:

        response = None

        usage = None

        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0

        for attempt in range(settings.MAX_RETRIES):

            try:

                logger.info(
                    f"LLM request attempt {attempt + 1}"
                )

                response = self.client.chat.completions.create(
                    model=settings.MODEL_NAME,
                    messages=messages,
                    temperature=settings.TEMPERATURE,
                    max_tokens=settings.MAX_TOKENS
                )

                usage = response.usage

                if usage is not None:
                    prompt_tokens = usage.prompt_tokens
                    completion_tokens = usage.completion_tokens
                    total_tokens = usage.total_tokens
                    logger.info(
                        f"Token Usage | "
                        f"Input={prompt_tokens} | "
                        f"Output={completion_tokens} | "
                        f"Total={total_tokens}"
                    )

                break

            except Exception as ex:

                logger.error(
                    f"Attempt {attempt + 1} failed: {str(ex)}"
                )

                if attempt == settings.MAX_RETRIES - 1:
                    raise LLMServiceError(
                        f"Failed after {settings.MAX_RETRIES} attempts"
                    )

                time.sleep(2)

        if not response.choices:
            raise LLMResponseError(
                "No choices returned by model"
            )

        content = response.choices[0].message.content

        if not content:
            raise LLMResponseError(
                "Empty response from model"
            )

        return LLMResponse(
            content=content,
            model=settings.MODEL_NAME,
            usage= UsageResponse(
                input_tokens= prompt_tokens,
                output_tokens= completion_tokens,
                total_tokens= total_tokens
            )
        )