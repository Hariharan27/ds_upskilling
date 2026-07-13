from fastapi import Depends

from app.application.tools.tool_executor import (
    ToolExecutor,
)
from app.domain.tools.tool_registry import (
    ToolRegistry,
)
from app.presentation.api.dependencies.tools import (
    get_tool_registry,
)


def get_tool_executor(
    tool_registry: ToolRegistry = Depends(
        get_tool_registry,
    ),
) -> ToolExecutor:

    return ToolExecutor(
        tool_registry=tool_registry,
    )