from app.application.services.action_argument_extraction.action_argument_extraction_service import \
    ActionArgumentExtractionService
from app.application.services.action_argument_extraction.models import ActionArgumentExtractionRequest
from app.application.services.action_validation.action_argument_validator import ActionArgumentValidator
from app.application.services.action_validation.action_clarification_service import ActionClarificationService
from app.application.services.chat.models import (
    ChatRequest,
    ChatResponse,
)
from app.application.services.response_generation.models import (
    ResponseGenerationRequest,
)
from app.application.services.response_generation.response_generation_service import (
    ResponseGenerationService,
)
from app.application.tools.tool_executor import (
    ToolExecutor,
)
from app.domain.enums.ExecutionType import ExecutionType
from app.domain.models.intent_classification_request import (
    IntentClassificationRequest,
)
from app.domain.models.tool_execution_request import (
    ToolExecutionRequest,
)
from app.domain.services.intent_classifier import (
    IntentClassifier,
)
from app.domain.tools.tool_registry import ToolRegistry


class ChatGenerationService:

    def __init__(
        self,
        response_generation_service: ResponseGenerationService,
        intent_classifier: IntentClassifier,
        tool_executor: ToolExecutor,
        tool_registry: ToolRegistry,
        action_argument_extraction_service: ActionArgumentExtractionService,
        action_clarification_service: ActionClarificationService,
        action_argument_validator: ActionArgumentValidator
    ) -> None:

        self._response_generation_service = (
            response_generation_service
        )
        self._intent_classifier = intent_classifier
        self._tool_executor = tool_executor
        self._tool_registry = tool_registry
        self._action_argument_extraction_service = action_argument_extraction_service
        self._action_clarification_service = action_clarification_service
        self._action_argument_validator = action_argument_validator

    def generate_chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        intent_request = IntentClassificationRequest(
            query=request.query,
            conversation_history=request.conversation_history,
        )

        classification = self._intent_classifier.classify(
            intent_request,
        )

        print(f"Classification: {classification}")

        if not classification.tool_name:
            return ChatResponse(
                answer="I'm sorry, I couldn't determine how to handle your request.",
                sources=None,
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
            )

        tool = self._tool_registry.get_tool(
            classification.tool_name,
        )

        print(f"Tool definition: {tool.definition}")

        if tool.definition.execution_type == ExecutionType.QUERY:
            tool_request = ToolExecutionRequest(
                query=request.query,
                conversation_history=request.conversation_history,
            )

            tool_result = self._tool_executor.execute(
                classification.tool_name,
                tool_request,
            )

            if not tool_result.success:
                return ChatResponse(
                    answer=tool_result.error_message or "An unexpected error occurred.",
                    sources=None,
                    input_tokens=0,
                    output_tokens=0,
                    total_tokens=0,
                )

            print(f"Context: {tool_result.context}")

            response_request = ResponseGenerationRequest(
                query=request.query,
                conversation_history=request.conversation_history,
                context=tool_result.context or "",
            )

            response = (
                self._response_generation_service.generate(
                    response_request,
                )
            )

            return ChatResponse(
                answer=response.answer,
                sources=tool_result.sources,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                total_tokens=response.total_tokens,
            )
        else:
            print(f"Action Started------>")
            extraction_request = ActionArgumentExtractionRequest(
                query=request.query,
                conversation_history=request.conversation_history,
                tool_definition=tool.definition,
            )
            arguments = (
                self._action_argument_extraction_service.extract(
                    extraction_request,
                )
            )
            print(f"Extracted Arguments: {arguments}")

            normalizer = tool.argument_normalizer

            if normalizer is not None:
                arguments = normalizer.normalize(
                    arguments,
                )

            print(f"Normalized Arguments: {arguments}")

            validation_result = None

            if tool.argument_validator is not None:
                validation_result = (
                    tool.argument_validator.validate(
                        arguments,
                    )
                )

            print(f"Validation Result: {validation_result}")

            if (
                    validation_result is not None
                    and not validation_result.is_valid
            ):
                clarification = (
                    self._action_clarification_service.build(
                        validation_result,
                    )
                )

                return ChatResponse(
                    answer=clarification,
                    sources=None,
                    input_tokens=0,
                    output_tokens=0,
                    total_tokens=0,
                )

            tool_result = self._tool_executor.execute(
                classification.tool_name,
                ToolExecutionRequest(
                    query=request.query,
                    conversation_history=request.conversation_history,
                    arguments=arguments,
                ),
            )

            if not tool_result.success:
                return ChatResponse(
                    answer=tool_result.error_message or "An unexpected error occurred.",
                    sources=None,
                    input_tokens=0,
                    output_tokens=0,
                    total_tokens=0,
                )

            response_request = ResponseGenerationRequest(
                query=request.query,
                conversation_history=request.conversation_history,
                context=tool_result.context or "",
            )

            response = (
                self._response_generation_service.generate(
                    response_request,
                )
            )

            return ChatResponse(
                answer=response.answer,
                sources=tool_result.sources,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                total_tokens=response.total_tokens,
            )

