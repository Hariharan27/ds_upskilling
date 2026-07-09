from fastapi import Depends

from app.application.services.rag.rag_generation_service import (
    RAGGenerationService,
)
from app.infrastructure.tools.search_documents_tool import (
    SearchDocumentsTool,
)
from app.domain.tools.tool_registry import (
    ToolRegistry,
)
from app.presentation.api.dependencies.rag import (
    get_rag_generation_service,
)
from app.presentation.api.dependencies.hrms import (
    get_hrms_rest_client,
    get_leave_details_request_mapper,
)
from app.infrastructure.tools.leave_balance_tool import (
    LeaveBalanceTool,
)
from app.domain.services.hrms_rest_client import (
    HRMSRestClient,
)
from app.infrastructure.rest.mappers.leave_details_request_mapper import (
    LeaveDetailsRequestMapper,
)
from app.application.tools.tool_executor import (
    ToolExecutor,
)


def get_tool_registry(
    rag_generation_service: RAGGenerationService = Depends(
        get_rag_generation_service,
    ),
    rest_client: HRMSRestClient = Depends(
        get_hrms_rest_client,
    ),

    leave_details_request_mapper: LeaveDetailsRequestMapper = Depends(
        get_leave_details_request_mapper,
    ),
) -> ToolRegistry:

    registry = ToolRegistry()

    registry.register_tool(
        SearchDocumentsTool(
            rag_generation_service=rag_generation_service,
        )
    )

    registry.register_tool(
        LeaveBalanceTool(
            rest_client=rest_client,
            request_mapper=leave_details_request_mapper,
        )
    )



    return registry


def get_tool_executor(
    tool_registry: ToolRegistry = Depends(
        get_tool_registry,
    ),
) -> ToolExecutor:

    return ToolExecutor(
        tool_registry=tool_registry,
    )