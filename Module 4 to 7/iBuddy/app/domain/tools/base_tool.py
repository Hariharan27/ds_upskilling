from abc import ABC
from abc import abstractmethod

from app.domain.models.tool_definition import (
    ToolDefinition,
)
from app.domain.models.tool_execution_request import (
    ToolExecutionRequest,
)
from app.domain.models.tool_execution_result import (
    ToolExecutionResult,
)
from app.application.services.action_validation.action_argument_validator import (
    ActionArgumentValidator,
)
from app.domain.services.action_argument_normalizer import ActionArgumentNormalizer

class BaseTool(ABC):

    @property
    @abstractmethod
    def definition(
        self,
    ) -> ToolDefinition:
        """
        Metadata describing this tool.
        """
        pass

    @abstractmethod
    def execute(
        self,
        request: ToolExecutionRequest,
    ) -> ToolExecutionResult:
        """
        Execute the tool.
        """
        pass

    @property
    def argument_normalizer(
            self,
    ) -> ActionArgumentNormalizer | None:
        return None

    @property
    def argument_validator(
            self,
    ) -> ActionArgumentValidator | None:
        return None


