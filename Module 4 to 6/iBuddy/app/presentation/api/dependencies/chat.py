from fastapi import Depends

from app.application.services.chat.chat_generation_service import ChatGenerationService
from app.application.services.rag.rag_generation_service import RAGGenerationService
from app.domain.services.intent_classifier import IntentClassifier
from app.domain.services.llm_client import LLMClient
from app.domain.tools.tool_registry import ToolRegistry
from app.presentation.api.dependencies.rag import get_rag_generation_service
from app.presentation.api.dependencies.tools import get_tool_registry
from app.application.services.intent.intent_prompt_builder import IntentPromptBuilder
from app.infrastructure.intent.llm_intent_classifier import LLMIntentClassifier
from app.presentation.api.dependencies.llm import get_client

def get_chat_generation_service(
        rag_generation_service: RAGGenerationService = Depends(
            get_rag_generation_service
        ),
) -> ChatGenerationService:
    return ChatGenerationService(
        rag_generation_service= rag_generation_service
    )


def get_intent_classifier(
    tool_registry: ToolRegistry = Depends(
        get_tool_registry,
    ),
    llm_client: LLMClient = Depends(
        get_client,
    ),
) -> IntentClassifier:

    prompt_builder = IntentPromptBuilder(
        tool_registry=tool_registry,
    )

    return LLMIntentClassifier(
        prompt_builder=prompt_builder,
        llm_client=llm_client,
    )