import time

from together import Together
from app.core.config import settings
from app.services.llm.models import (
    LLMResponse
)
from  app.services.llm.exceptions import (
LLMServiceError,
LLMResponseError
)
from together.types.chat import completion_create_params



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

        for attempt in range(settings.MAX_RETRIES):

            try:

                print(
                    f"LLM request attempt {attempt + 1}"
                )

                response = self.client.chat.completions.create(
                    model=settings.MODEL_NAME,
                    messages=messages,
                    temperature=settings.TEMPERATURE,
                    max_tokens=settings.MAX_TOKENS
                )

                break

            except Exception as ex:

                print(
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
            model=settings.MODEL_NAME
        )