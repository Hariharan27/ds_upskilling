import json

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
            name="get_leave_details",
            description=(
                "Purpose:\n"
                "Retrieve the authenticated employee's personal leave information "
                "from the HRMS system.\n\n"

                "Use this tool whenever the user asks about their own leave data, "
                "including leave balances, leave usage, leave history, leave dates, "
                "leave eligibility, or leave details.\n\n"

                "Use When:\n"
                "- How many earned leaves do I have?\n"
                "- How many casual leaves do I have?\n"
                "- How many sick leaves do I have?\n"
                "- How many privilege leaves do I have?\n"
                "- What is my leave balance?\n"
                "- How many earned leaves have I taken?\n"
                "- How many casual leaves have I taken?\n"
                "- How many sick leaves have I taken?\n"
                "- How many privilege leaves have I taken?\n"
                "- How many paternity leaves have I taken?\n"
                "- When did I take paternity leave?\n"
                "- Show my leave history.\n"
                "- Which dates did I take casual leave?\n"
                "- Which dates did I take sick leave?\n"
                "- Which dates did I take privilege leave?\n"
                "- Which dates did I take earned leave?\n"
                "- Which dates did I take paternity leave?\n"
                "- Show all my taken leaves.\n"
                "- Which leave type has the highest balance?\n"
                "- How many leave days are eligible?\n"
                "- How many leaves have expired?\n"
                "- Show my leave details.\n\n"

                "Supported Leave Types:\n"
                "- Earned Leave\n"
                "- Casual Leave\n"
                "- Sick Leave\n"
                "- Privilege Leave\n"
                "- Paternity Leave\n"
                "- Any leave type returned by the HRMS response.\n\n"

                "Do Not Use When:\n"
                "- Questions about leave policy.\n"
                "- Questions about company HR policy.\n"
                "- Questions about leave rules or documentation.\n"
                "- Questions about WFH policy or any enterprise document."
            ),
            execution_type= ExecutionType.QUERY,
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

        context = json.dumps(
            response["entity"],
            indent=2,
        )
        return ToolExecutionResult(
            success=True,
            context=context,
            sources=None,
            data= {
                "entity": response["entity"],
            },
        )