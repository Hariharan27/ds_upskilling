from app.application.services.chat.models import (
    ChatRequest,
    ChatResponse,
)
from app.application.services.rag.models import (
    RAGRequest,
)
from app.application.services.rag.rag_generation_service import RAGGenerationService
from app.domain.models.intent_classification_request import IntentClassificationRequest
from app.domain.models.tool_execution_request import ToolExecutionRequest
from app.domain.services.intent_classifier import IntentClassifier
from app.application.tools.tool_executor import ToolExecutor


class ChatGenerationService:

    def __init__(
            self,
            rag_generation_service: RAGGenerationService,
            intent_classifier: IntentClassifier,
            tool_executor: ToolExecutor,
    ):
        self.rag_generation_service = rag_generation_service
        self.intent_classifier = intent_classifier
        self.tool_executor = tool_executor


    def generate_chat(self,request: ChatRequest) -> ChatResponse:

        intent_request = IntentClassificationRequest(
            query=request.query,
            conversation_history=request.conversation_history,
        )

        classification = self.intent_classifier.classify(
            intent_request,
        )

        tool_request = ToolExecutionRequest(
            query=request.query,
            conversation_history=request.conversation_history,
        )

        tool_result = self.tool_executor.execute(
            classification.tool_name,
            tool_request,
        )

        rag_request = RAGRequest(
            query=request.query,
            conversation_history=request.conversation_history,
        )

        rag_response = self.rag_generation_service.generate(rag_request)

        return ChatResponse(
            answer= rag_response.answer,
            sources=rag_response.sources,
            input_tokens= rag_response.input_tokens,
            output_tokens= rag_response.output_tokens,
            total_tokens= rag_response.total_tokens,
        )
