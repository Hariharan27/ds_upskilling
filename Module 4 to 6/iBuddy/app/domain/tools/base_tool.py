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