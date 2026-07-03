from pydantic import BaseModel

from app.schemas.enums import (
    CategoryEnum,
    DepartmentEnum,
    PriorityEnum,
)


class UsageResponse(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class TicketClassificationResponse(BaseModel):
    department: DepartmentEnum
    category: CategoryEnum
    priority: PriorityEnum
    summary: str
    employee_response: str


class CostResponse(BaseModel):
    input_cost_usd: float
    output_cost_usd: float
    total_cost_usd: float


class ClassificationApiResponse(BaseModel):
    classification: TicketClassificationResponse
    usage: UsageResponse
    cost: CostResponse
    prompt_version: str