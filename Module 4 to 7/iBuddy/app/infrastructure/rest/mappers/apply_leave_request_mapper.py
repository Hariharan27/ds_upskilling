from app.application.services.action_argument_extraction.models import (
    ApplyLeaveArguments,
)
from app.infrastructure.rest.models.apply_leave_request import (
    ApplyLeaveRequest,
)


class ApplyLeaveRequestMapper:

    def map(
        self,
        arguments: ApplyLeaveArguments,
    ) -> ApplyLeaveRequest:

        return ApplyLeaveRequest(
            leaveStartDate=arguments.leave_start_date,
            leaveEndDate=arguments.leave_end_date,
            leaveReason=arguments.leave_reason,
            leaveType=arguments.leave_type,
            employeeId="386",          # TODO: Fetch from authenticated user profile
        )