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
from app.domain.models.intent_classification_request import (
    IntentClassificationRequest,
)
from app.domain.models.tool_execution_request import (
    ToolExecutionRequest,
)
from app.domain.services.intent_classifier import (
    IntentClassifier,
)


class ChatGenerationService:

    def __init__(
        self,
        response_generation_service: ResponseGenerationService,
        intent_classifier: IntentClassifier,
        tool_executor: ToolExecutor,
    ) -> None:

        self._response_generation_service = (
            response_generation_service
        )
        self._intent_classifier = intent_classifier
        self._tool_executor = tool_executor

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

        if not classification.tool_name:
            return ChatResponse(
                answer="I'm sorry, I couldn't determine how to handle your request.",
                sources=None,
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
            )

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