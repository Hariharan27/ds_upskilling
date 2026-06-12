from fastapi import APIRouter

from app.schemas.request import (
    TicketClassificationRequest
)

from app.schemas.response import (
    TicketClassificationResponse
)

from app.services.classification.classifier_service import (
    ClassifierService
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

    service = ClassifierService()

    return service.classify(
        employee_message=request.message
    )

