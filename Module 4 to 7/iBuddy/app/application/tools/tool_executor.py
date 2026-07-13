from app.domain.models.tool_execution_request import (
    ToolExecutionRequest,
)
from app.domain.models.tool_execution_result import (
    ToolExecutionResult,
)
from app.domain.tools.tool_registry import (
    ToolRegistry,
)


class ToolExecutor:

    def __init__(
        self,
        tool_registry: ToolRegistry,
    ) -> None:

        self._tool_registry = tool_registry

    def execute(
        self,
        tool_name: str,
        request: ToolExecutionRequest,
    ) -> ToolExecutionResult:

        tool = self._tool_registry.get_tool(
            tool_name,
        )

        if tool is None:
            raise ValueError(
                f"Tool '{tool_name}' is not registered."
            )

        return tool.execute(
            request,
        )