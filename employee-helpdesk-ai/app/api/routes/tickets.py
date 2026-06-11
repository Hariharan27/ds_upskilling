from fastapi import APIRouter

from app.schemas.request import (
    TicketClassificationRequest
)

from app.schemas.response import (
    TicketClassificationResponse
)

from app.schemas.enums import (
    DepartmentEnum,
    CategoryEnum,
    PriorityEnum
)

router = APIRouter()


@router.post(
    "/tickets/classify",
    response_model=TicketClassificationResponse
)
async def classify_ticket(
    request: TicketClassificationRequest
):

    return TicketClassificationResponse(
        department=DepartmentEnum.IT_SUPPORT,
        category=CategoryEnum.VPN_ACCESS,
        priority=PriorityEnum.MEDIUM,
        summary="Temporary response",
        employee_response="Temporary response"
    )