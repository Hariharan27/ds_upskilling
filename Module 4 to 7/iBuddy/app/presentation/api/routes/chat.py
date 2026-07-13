from fastapi import APIRouter
from fastapi import Depends


from app.presentation.api.dependencies.chat import (
    get_chat_generation_service,
)
from app.presentation.api.models.chat import (
    ChatRequest,
    ChatResponse,
)
from app.application.services.chat.chat_generation_service import (
    ChatGenerationService,
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
    chat_service: ChatGenerationService = Depends(
        get_chat_generation_service,
    ),
) -> ChatResponse:

    response = chat_service.generate_chat(
        request=request,
    )

    return ChatResponse(
        answer=response.answer,
        sources=response.sources,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        total_tokens=response.total_tokens,
    )