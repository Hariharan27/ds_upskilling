from fastapi import Depends

from app.application.services.action_argument_extraction.relative_date_resolver import RelativeDateResolver
from app.application.services.action_normalization.apply_leave_argument_normalizer import ApplyLeaveArgumentNormalizer
from app.application.services.action_validation.apply_leave_argument_validator import ApplyLeaveArgumentValidator
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
from app.infrastructure.rest.mappers.apply_leave_response_mapper import ApplyLeaveResponseMapper
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
    get_leave_details_request_mapper, get_apply_leave_response_mapper,
)
from app.presentation.api.dependencies.multi_query_retrieval import (
    get_multi_query_retrieval_service,
)


def get_argument_validator():
    return ApplyLeaveArgumentValidator()

def get_relative_date_resolver() -> RelativeDateResolver:
    return RelativeDateResolver()

def get_apply_leave_argument_normalizer(
        relative_date_resolver: RelativeDateResolver = Depends(
            get_relative_date_resolver,
        )
) -> ApplyLeaveArgumentNormalizer:

    return ApplyLeaveArgumentNormalizer(relative_date_resolver=relative_date_resolver)


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
    apply_leave_response_mapper: ApplyLeaveResponseMapper = Depends(
        get_apply_leave_response_mapper
    ),
    apply_leave_argument_normalizer: ApplyLeaveArgumentNormalizer = Depends(
        get_apply_leave_argument_normalizer
    ),
    apply_leave_argument_validator: ApplyLeaveArgumentValidator = Depends(
        get_argument_validator
    )
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
            response_mapper= apply_leave_response_mapper,
            argument_normalizer=apply_leave_argument_normalizer,
            argument_validator=apply_leave_argument_validator,
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

