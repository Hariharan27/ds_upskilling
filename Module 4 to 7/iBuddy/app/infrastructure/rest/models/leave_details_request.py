from pydantic import BaseModel


class LeaveDetailsRequest(BaseModel):
    year: int
    quarter: int