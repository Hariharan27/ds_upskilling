from fastapi import Depends

from app.application.services.retrieval.multi_query_retrieval_service import (
    MultiQueryRetrievalService,
)
from app.application.tools.tool_executor import (
    ToolExecutor,
)
from app.domain.services.context_builder import (
    ContextBuilder,
)
from app.domain.services.hrms_rest_client import (
    HRMSRestClient,
)
from app.domain.tools.tool_registry import (
    ToolRegistry,
)
from app.infrastructure.rest.mappers.apply_leave_request_mapper import (
    ApplyLeaveRequestMapper,
)
from app.infrastructure.rest.mappers.leave_details_request_mapper import (
    LeaveDetailsRequestMapper,
)
from app.infrastructure.tools.apply_leave_tool import (
    ApplyLeaveTool,
)
from app.infrastructure.tools.leave_balance_tool import (
    LeaveBalanceTool,
)
from app.infrastructure.tools.search_documents_tool import (
    SearchDocumentsTool,
)
from app.presentation.api.dependencies.context_builder import (
    get_context_builder,
)
from app.presentation.api.dependencies.hrms import (
    get_apply_leave_request_mapper,
    get_hrms_rest_client,
    get_leave_details_request_mapper,
)
from app.presentation.api.dependencies.multi_query_retrieval import (
    get_multi_query_retrieval_service,
)


def get_tool_registry(
    retrieval_service: MultiQueryRetrievalService = Depends(
        get_multi_query_retrieval_service,
    ),
    context_builder: ContextBuilder = Depends(
        get_context_builder,
    ),
    rest_client: HRMSRestClient = Depends(
        get_hrms_rest_client,
    ),
    leave_details_request_mapper: LeaveDetailsRequestMapper = Depends(
        get_leave_details_request_mapper,
    ),
    apply_leave_request_mapper: ApplyLeaveRequestMapper = Depends(
        get_apply_leave_request_mapper,
    ),
) -> ToolRegistry:

    registry = ToolRegistry()

    registry.register_tool(
        SearchDocumentsTool(
            retrieval_service=retrieval_service,
            context_builder=context_builder,
        )
    )

    registry.register_tool(
        LeaveBalanceTool(
            rest_client=rest_client,
            request_mapper=leave_details_request_mapper,
        )
    )

    registry.register_tool(
        ApplyLeaveTool(
            rest_client=rest_client,
            request_mapper=apply_leave_request_mapper,
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