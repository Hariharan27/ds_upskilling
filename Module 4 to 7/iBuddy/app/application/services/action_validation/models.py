from pydantic import BaseModel,Field

class ValidationError(
    BaseModel,
):
    field: str
    code: str

class ActionValidationResult(
    BaseModel,
):
    is_valid: bool

    missing_fields: list[str] = Field(
        default_factory=list,
    )

    invalid_fields: list[
        ValidationError
    ] = Field(
        default_factory=list,
    )

