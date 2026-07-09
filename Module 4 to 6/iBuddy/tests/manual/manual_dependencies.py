from app.domain.tools.tool_registry import (
    ToolRegistry,
)
from app.infrastructure.rest.hrms_rest_client import (
    HRMSRestClientImpl,
)
from app.infrastructure.rest.mappers.leave_details_request_mapper import (
    LeaveDetailsRequestMapper,
)
from app.infrastructure.system.system_date_provider import (
    SystemDateProvider,
)
from app.infrastructure.tools.leave_balance_tool import (
    LeaveBalanceTool,
)
from app.infrastructure.tools.search_documents_tool import (
    SearchDocumentsTool,
)
from app.presentation.api.dependencies.rag import (
    get_rag_generation_service,
)
from app.application.tools.tool_executor import (
    ToolExecutor,
)
from app.application.services.intent.intent_prompt_builder import (
    IntentPromptBuilder,
)
from app.infrastructure.intent.llm_intent_classifier import (
    LLMIntentClassifier,
)
from app.presentation.api.dependencies.llm import (
    get_client,
)



def get_manual_intent_classifier() -> LLMIntentClassifier:

    tool_registry = get_manual_tool_registry()

    prompt_builder = IntentPromptBuilder(
        tool_registry=tool_registry,
    )

    return LLMIntentClassifier(
        prompt_builder=prompt_builder,
        llm_client=get_client(),
    )

def get_manual_tool_registry() -> ToolRegistry:

    registry = ToolRegistry()

    rag_generation_service = get_rag_generation_service()

    search_documents_tool = SearchDocumentsTool(
        rag_generation_service=rag_generation_service,
    )

    registry.register_tool(
        search_documents_tool,
    )

    date_provider = SystemDateProvider()

    request_mapper = LeaveDetailsRequestMapper(
        date_provider=date_provider,
    )

    rest_client = HRMSRestClientImpl()

    leave_balance_tool = LeaveBalanceTool(
        rest_client=rest_client,
        request_mapper=request_mapper,
    )

    registry.register_tool(
        leave_balance_tool,
    )

    return registry


def get_manual_tool_executor() -> ToolExecutor:

    tool_registry = get_manual_tool_registry()

    return ToolExecutor(
        tool_registry=tool_registry,
    )
