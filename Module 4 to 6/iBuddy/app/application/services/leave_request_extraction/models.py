from typing import Literal

from pydantic import BaseModel


class ApplyLeaveArguments(BaseModel):

    leave_type: Literal[
        "Work From Home",
        "Casual Leave",
        "Sick Leave",
        "Privilege Leave"
    ]

    leave_start_date: str

    leave_end_date: str

    leave_reason: str