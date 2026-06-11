from pydantic import BaseModel, Field


class TicketClassificationRequest(BaseModel):

    employee_id: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    message: str = Field(
        ...,
        min_length=10,
        max_length=2000
    )