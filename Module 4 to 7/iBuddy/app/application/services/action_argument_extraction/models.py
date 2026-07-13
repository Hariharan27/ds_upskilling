from typing import Literal

from pydantic import BaseModel, Field

from app.application.services.action_validation.models import ActionValidationResult
from app.domain.models.chat_message import ChatMessage
from app.domain.models.tool_definition import ToolDefinition

class ApplyLeaveArguments(BaseModel):

    leave_type: (
        Literal[
            "Work From Home",
            "Casual Leave",
            "Sick Leave",
            "Privilege Leave",
        ]
        | None
    ) = None

    leave_start_date: str | None = None

    leave_end_date: str | None = None

    leave_duration: str | None = None

    leave_reason: str | None = None


class ActionArgumentExtractionRequest(BaseModel):
    query: str
    conversation_history: list[ChatMessage] = Field(
        default_factory=list,
    )
    tool_definition: ToolDefinition

class ActionArgumentExtractionResult(BaseModel):
    arguments: ApplyLeaveArguments

    validation_result: ActionValidationResult