from fastapi import Depends

from app.application.services.chat.chat_generation_service import ChatGenerationService
from app.application.services.response_generation.response_generation_service import ResponseGenerationService
from app.application.tools.tool_executor import ToolExecutor
from app.presentation.api.dependencies.response_generation import get_response_generation_service
from app.presentation.api.dependencies.tool_executor import get_tool_executor
from app.domain.services.intent_classifier import IntentClassifier
from app.domain.services.llm_client import LLMClient
from app.domain.tools.tool_registry import ToolRegistry
from app.presentation.api.dependencies.tools import get_tool_registry
from app.application.services.intent.intent_prompt_builder import IntentPromptBuilder
from app.infrastructure.intent.llm_intent_classifier import LLMIntentClassifier
from app.presentation.api.dependencies.llm import get_client

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

def get_chat_generation_service(
    response_generation_service: ResponseGenerationService = Depends(
        get_response_generation_service,
    ),
    intent_classifier: IntentClassifier = Depends(
        get_intent_classifier,
    ),
    tool_executor: ToolExecutor = Depends(
        get_tool_executor,
    ),
) -> ChatGenerationService:

    return ChatGenerationService(
        response_generation_service=response_generation_service,
        intent_classifier=intent_classifier,
        tool_executor=tool_executor,
    )


