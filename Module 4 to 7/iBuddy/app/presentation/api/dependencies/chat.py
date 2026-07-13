from fastapi import Depends

from app.application.services.action_argument_extraction.action_argument_extraction_service import \
    ActionArgumentExtractionService
from app.application.services.action_argument_extraction.action_argument_prompt_builder import \
    ActionArgumentPromptBuilder
from app.application.services.action_argument_extraction.field_metadata import ACTION_ARGUMENT_FIELD_LABELS
from app.application.services.action_validation.action_argument_validator import ActionArgumentValidator
from app.application.services.action_validation.action_clarification_service import ActionClarificationService
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
from app.application.services.action_validation.apply_leave_argument_validator import (
    ApplyLeaveArgumentValidator,
)

def get_apply_leave_argument_validator(
) -> ApplyLeaveArgumentValidator:

    return ApplyLeaveArgumentValidator()

def get_action_argument_extraction_service(
    llm_client: LLMClient = Depends(
        get_client,
    ),
) -> ActionArgumentExtractionService:

    return ActionArgumentExtractionService(
        llm_client=llm_client,
        prompt_builder=ActionArgumentPromptBuilder()
    )

def get_action_clarification_service(
) -> ActionClarificationService:
    return ActionClarificationService(
        field_labels=ACTION_ARGUMENT_FIELD_LABELS,
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

def get_action_argument_validator(
) -> ActionArgumentValidator:

    return ActionArgumentValidator()


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
    tool_registry: ToolRegistry = Depends(
        get_tool_registry,
    ),
    action_argument_extraction_service: ActionArgumentExtractionService = Depends(
        get_action_argument_extraction_service,
    ),
    action_clarification_service: ActionClarificationService = Depends(
        get_action_clarification_service,
    ),
    action_argument_validator: ActionArgumentValidator = Depends(
        get_action_argument_validator,
    ),
) -> ChatGenerationService:

    return ChatGenerationService(
        response_generation_service=response_generation_service,
        intent_classifier=intent_classifier,
        tool_executor=tool_executor,
        action_argument_extraction_service=action_argument_extraction_service,
        action_clarification_service=action_clarification_service,
        tool_registry=tool_registry,
        action_argument_validator=action_argument_validator,
    )



