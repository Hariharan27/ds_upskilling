from app.infrastructure.rest.models.apply_leave_request import (
    ApplyLeaveRequest,
)


class ApplyLeaveRequestMapper:

    def map(
        self,
    ) -> ApplyLeaveRequest:

        return ApplyLeaveRequest(
            leaveStartDate="2026-07-07T00:00:00",
            leaveEndDate="2026-07-07T00:00:00",
            leaveReason="Applied via iBuddy",
            leaveType="Work From Home",
            reportingManagerIds=[9],
            employeeId="386",
        )