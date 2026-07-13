from typing import cast

from app.application.services.action_argument_extraction.models import (
    ApplyLeaveArguments,
)
from app.application.services.action_normalization.apply_leave_argument_normalizer import ApplyLeaveArgumentNormalizer
from app.application.services.action_validation.apply_leave_argument_validator import ApplyLeaveArgumentValidator
from app.domain.enums.ExecutionType import ExecutionType
from app.domain.enums.http_method import HttpMethod
from app.domain.models.tool_definition import (
    ToolDefinition,
)
from app.domain.models.tool_execution_request import (
    ToolExecutionRequest,
)
from app.domain.models.tool_execution_result import (
    ToolExecutionResult,
)
from app.domain.services.hrms_rest_client import (
    HRMSRestClient,
)
from app.domain.tools.base_tool import (
    BaseTool,
)
from app.infrastructure.rest.mappers.apply_leave_request_mapper import (
    ApplyLeaveRequestMapper,
)
from app.infrastructure.rest.mappers.apply_leave_response_mapper import ApplyLeaveResponseMapper
from app.shared.constants.hrms_api import (
    HRMSApiEndpoints,
)


class ApplyLeaveTool(BaseTool):

    def __init__(
        self,
        rest_client: HRMSRestClient,
        request_mapper: ApplyLeaveRequestMapper,
        response_mapper: ApplyLeaveResponseMapper,
        argument_normalizer: ApplyLeaveArgumentNormalizer,
        argument_validator: ApplyLeaveArgumentValidator,
    ) -> None:

        self._rest_client = rest_client
        self._request_mapper = request_mapper
        self._response_mapper = response_mapper
        self._argument_normalizer = argument_normalizer
        self._argument_validator = argument_validator

    @property
    def definition(
        self,
    ) -> ToolDefinition:

        return ToolDefinition(
            name="apply_leave",
            description=(
                "Purpose:\n"
                "Submit a leave request or Work From Home request "
                "for the authenticated employee.\n\n"

                "Use When:\n"
                "- User wants to apply for leave.\n"
                "- User wants to request Work From Home.\n"
                "- User wants to submit a leave application.\n"
                "- User asks to create a leave request.\n\n"

                "Required Information:\n"
                "- Leave type.\n"
                "- Start date.\n"
                "- End date.\n"
                "- Leave reason.\n\n"

                "Do Not Use When:\n"
                "- User asks about leave balance.\n"
                "- User asks about leave policy.\n"
                "- User asks about company HR policies.\n"
                "- User only wants information without creating a request."
            ),
            execution_type=ExecutionType.ACTION,
            argument_schema=ApplyLeaveArguments,
            argument_normalizer = ApplyLeaveArgumentNormalizer,

        )

    def _is_valid_response(
        self,
        response: dict,
    ) -> bool:

        return (
            response.get("entity") is not None
        )

    def execute(
        self,
        request: ToolExecutionRequest,
    ) -> ToolExecutionResult:

        if request.arguments is None:
            return ToolExecutionResult(
                success=False,
                error_message="Missing action arguments.",
            )

        arguments = cast(
            ApplyLeaveArguments,
            request.arguments,
        )

        apply_leave_request = (
            self._request_mapper.map(
                arguments,
            )
        )

        response = self._rest_client.execute(
            endpoint=HRMSApiEndpoints.APPLY_LEAVE,
            method=HttpMethod.POST,
            payload=apply_leave_request.model_dump(),
        )

        if not self._is_valid_response(
            response,
        ):
            return ToolExecutionResult(
                success=False,
                error_message="Unable to submit the leave request.",
            )

        return ToolExecutionResult(
            success=True,
            context=self._response_mapper.map(
                response,
            ),
            sources=None,
            data={
                "entity": response["entity"],
            },
        )

    @property
    def argument_normalizer(
            self,
    ) -> ApplyLeaveArgumentNormalizer:

        return self._argument_normalizer

    @property
    def argument_validator(
            self,
    ) -> ApplyLeaveArgumentValidator:

        return self._argument_validator