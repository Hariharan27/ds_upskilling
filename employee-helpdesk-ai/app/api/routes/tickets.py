from fastapi import APIRouter

from app.schemas.request import TicketClassificationRequest

from app.schemas.response import ClassificationApiResponse

from app.services.classification.classifier_service import ClassifierService


router = APIRouter()


@router.post("/tickets/classify", response_model=ClassificationApiResponse)
async def classify_ticket(
    request: TicketClassificationRequest
):
    service = ClassifierService()

    return service.classify(employee_message=request.message)

