from fastapi import APIRouter
from fastapi import Depends

from app.application.services.rag.models import (
    RAGRequest,
)
from app.presentation.api.dependencies.rag import (
    get_rag_generation_service,
)
from app.presentation.api.models.chat import (
    ChatRequest,
    ChatResponse,
)
from app.application.services.rag.rag_generation_service import (
    RAGGenerationService,
)

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)

@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    rag_service: RAGGenerationService = Depends(
        get_rag_generation_service,
    ),
) -> ChatResponse:

    rag_request = RAGRequest(
        query=request.query,
        conversation_history=request.conversation_history,
    )

    response = rag_service.generate(
        rag_request,
    )

    return ChatResponse(
        answer=response.answer,
        sources=response.sources,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        total_tokens=response.total_tokens,
    )