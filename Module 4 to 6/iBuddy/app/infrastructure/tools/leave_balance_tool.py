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
from app.domain.services.hrms_rest_client import HRMSRestClient
from app.domain.tools.base_tool import (
    BaseTool,
)
from app.infrastructure.rest.mappers.leave_details_request_mapper import LeaveDetailsRequestMapper
from app.shared.constants.hrms_api import (
    HRMSApiEndpoints,
)


class LeaveBalanceTool(BaseTool):

    def __init__(
            self,
            rest_client: HRMSRestClient,
            request_mapper: LeaveDetailsRequestMapper,
    ) -> None:
        self._rest_client = rest_client
        self._request_mapper = request_mapper

    @property
    def definition(
        self,
    ) -> ToolDefinition:

        return ToolDefinition(
            name="get_leave_balance",
            description=(
                "Purpose:\n"
                "Retrieve the authenticated employee's leave balance.\n\n"
                "Use When:\n"
                "- User asks for remaining leave.\n"
                "- User asks for earned leave balance.\n"
                "- User asks for casual leave balance.\n"
                "- User asks for sick leave balance.\n\n"
                "Do Not Use When:\n"
                "- Questions about leave policy.\n"
                "- Questions about company HR policy.\n"
                "- Questions about leave rules or documentation."
            ),
        )

    def _is_valid_response(
            self,
            response: dict,
    ) -> bool:
        return (
                response.get("responseCode") == 200
                and response.get("entity") is not None
        )

    def execute(
        self,
        request: ToolExecutionRequest,
    ) -> ToolExecutionResult:

        leave_details_request = (
            self._request_mapper.map()
        )

        response = self._rest_client.execute(
            endpoint=HRMSApiEndpoints.LEAVE_DETAILS,
            method=HttpMethod.GET,
            query_params=leave_details_request.model_dump(),
        )

        if not self._is_valid_response(
                response,
        ):
            return ToolExecutionResult(
                success=False,
                error_message="Unable to retrieve leave details.",
            )

        return ToolExecutionResult(
            success=True,
            data=response["entity"],
        )