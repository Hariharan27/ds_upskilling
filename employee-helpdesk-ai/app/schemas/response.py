from pydantic import BaseModel

from app.schemas.enums import (
    DepartmentEnum,
    CategoryEnum,
    PriorityEnum
)


class TicketClassificationResponse(BaseModel):

    department: DepartmentEnum

    category: CategoryEnum

    priority: PriorityEnum

    summary: str

    employee_response: str