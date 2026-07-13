from app.application.services.action_argument_extraction.models import (
    ActionArgumentExtractionRequest,
)
from app.application.services.action_argument_extraction.prompts import (
    ACTION_ARGUMENT_EXTRACTION_SYSTEM_PROMPT,
    ACTION_ARGUMENT_EXTRACTION_USER_PROMPT_TEMPLATE,
)
from app.domain.models.chat_message import (
    ChatMessage,
    MessageRole,
)
from app.domain.models.llm_request import (
    LLMRequest,
)


class ActionArgumentPromptBuilder:
    """
    Builds the LLM request for ACTION argument extraction.
    """

    def build(
        self,
        request: ActionArgumentExtractionRequest,
    ) -> LLMRequest:
        messages: list[ChatMessage] = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=ACTION_ARGUMENT_EXTRACTION_SYSTEM_PROMPT,
            )
        ]

        messages.extend(
            request.conversation_history,
        )

        messages.append(
            ChatMessage(
                role=MessageRole.USER,
                content=self._build_user_prompt(
                    query=request.query,
                    tool_name=request.tool_definition.name,
                    tool_description=request.tool_definition.description,
                    schema=request.tool_definition.argument_schema.model_json_schema()
                ),
            )
        )

        return LLMRequest(
            messages=messages,
            response_schema=request.tool_definition.argument_schema,
        )

    def _build_user_prompt(
            self,
            query: str,
            tool_name: str,
            tool_description: str,
            schema: type[ActionArgumentExtractionRequest],
    ) -> str:
        """
        Build the user prompt for ACTION argument extraction.
        """

        return ACTION_ARGUMENT_EXTRACTION_USER_PROMPT_TEMPLATE.format(
            tool_name=tool_name,
            tool_description=tool_description,
            user_query=query,
            schema=schema,
        )