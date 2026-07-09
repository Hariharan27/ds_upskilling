from pydantic import BaseModel

class ApplyLeaveRequest(BaseModel):
    leaveEndDate: str
    leaveReason: str
    leaveStartDate: str
    leaveType: str
    reportingManagerIds: list[int]
    employeeId: str