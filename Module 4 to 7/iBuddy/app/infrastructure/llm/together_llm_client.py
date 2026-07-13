import time

from pydantic import BaseModel, ValidationError
from typing import Any
from together import Together
from together.types.chat import completion_create_params
from together.types.chat.completion_create_params import (
    MessageChatCompletionSystemMessageParam,
    MessageChatCompletionUserMessageParam,
    MessageChatCompletionAssistantMessageParam, ResponseFormatJsonSchema, ResponseFormatJsonSchemaJsonSchema,
)

from app.domain.models.chat_message import MessageRole
from app.domain.models.llm_request import (
    LLMRequest,
)
from app.domain.models.llm_response import (
    LLMResponse,
)
from app.domain.services.llm_client import (
    LLMClient,
)
from app.shared.config import (
    get_settings,
)
from app.shared.exceptions.llm import (
    LLMClientError,
    LLMResponseError,
)


class TogetherLLMClient(
    LLMClient,
):
    """
    Together AI implementation
    of the LLMClient.
    """

    def __init__(self) -> None:

        self._settings = get_settings()

        if not self._settings.together_api_key:
            raise ValueError(
                "TOGETHER_API_KEY is not configured."
            )

        self._client = Together(
            api_key=self._settings.together_api_key,
        )

    def _generate_completion(
            self,
            request: LLMRequest,
    )-> Any:
        """
        Generate a raw completion response from Together AI.
        """

        response = None

        for attempt in range(
                self._settings.max_retries,
        ):
            try:
                completion_kwargs: dict[str, Any] = {
                    "model": self._settings.together_model,
                    "messages": self._build_messages(request),
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens,
                }

                if request.response_schema is not None:
                    completion_kwargs["response_format"] = (
                        ResponseFormatJsonSchema(
                            type="json_schema",
                            json_schema=ResponseFormatJsonSchemaJsonSchema(
                                name=request.response_schema.__name__,
                                description=(
                                    f"Structured output for {request.response_schema.__name__}."
                                ),
                                schema=request.response_schema.model_json_schema(),
                                strict=True,
                            ),
                        )
                    )

                response = self._client.chat.completions.create(
                    **completion_kwargs,
                )

                print("\n" + "=" * 80)
                print("RAW TOGETHER RESPONSE")
                print("=" * 80)

                print(response.model_dump())

                print("=" * 80)
                print("MESSAGE")
                print("=" * 80)

                print(response.choices[0].message)

                print("=" * 80)
                print("FINISH REASON")
                print("=" * 80)

                print(response.choices[0].finish_reason)

                print("=" * 80)

                break

            except Exception as ex:

                if (
                        attempt
                        == self._settings.max_retries - 1
                ):
                    raise LLMClientError(
                        "Failed to generate LLM response."
                    ) from ex

                time.sleep(
                    self._settings.retry_delay_seconds,
                )

        if response is None:
            raise LLMClientError(
                "No response received from Together AI."
            )

        if not response.choices:
            raise LLMResponseError(
                "No choices returned by Together AI."
            )

        return response

    def generate_text(
            self,
            request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a natural language response.
        """

        response = self._generate_completion(
            request,
        )

        content = (
            response.choices[0]
            .message.content
        )

        if not content:
            raise LLMResponseError(
                "Empty response returned by Together AI."
            )

        usage = response.usage

        return LLMResponse(
            content=content,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )

    @staticmethod
    def _build_messages(
            request: LLMRequest,
    ) -> list[completion_create_params.Message]:

        messages: list[completion_create_params.Message] = []

        for message in request.messages:

            if message.role == MessageRole.SYSTEM.value:

                messages.append(
                    MessageChatCompletionSystemMessageParam(
                        role= MessageRole.SYSTEM.value,
                        content=message.content,
                    )
                )

            elif message.role == MessageRole.USER.value:

                messages.append(
                    MessageChatCompletionUserMessageParam(
                        role= MessageRole.USER.value,
                        content=message.content,
                    )
                )

            elif message.role == MessageRole.ASSISTANT.value:

                messages.append(
                    MessageChatCompletionAssistantMessageParam(
                        role=MessageRole.ASSISTANT.value,
                        content=message.content,
                    )
                )

        return messages

    def generate_structured(
            self,
            request: LLMRequest,
    ) -> BaseModel:
        """
        Generate a structured response using the provided schema.
        """

        if request.response_schema is None:
            raise ValueError(
                "response_schema must be provided for structured generation."
            )

        response = self._generate_completion(
            request,
        )

        content = (
            response.choices[0]
            .message.content
        )

        if not content:
            raise LLMResponseError(
                "Empty response returned by Together AI."
            )

        try:
            return request.response_schema.model_validate_json(
                content,
            )

        except ValidationError as ex:
            raise LLMResponseError(
                "Failed to parse structured LLM response."
            ) from ex

