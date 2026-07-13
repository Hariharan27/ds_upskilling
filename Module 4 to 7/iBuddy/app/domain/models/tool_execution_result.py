from pydantic import BaseModel
from pydantic import Field


class ToolExecutionResult(BaseModel):

    success: bool

    context: str | None = None

    sources: list[str] | None = None

    data: dict = Field(default_factory=dict,
    )
    error_message: str | None = None