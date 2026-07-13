from pydantic import BaseModel

from app.domain.enums.ExecutionType import ExecutionType
from app.domain.services.action_argument_normalizer import ActionArgumentNormalizer


class ToolDefinition(BaseModel):
    name:str
    description:str
    execution_type: ExecutionType
    argument_schema: type[BaseModel] | None = None
    argument_normalizer: type[ActionArgumentNormalizer] | None = None