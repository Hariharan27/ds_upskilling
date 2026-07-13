
from app.domain.tools.base_tool import BaseTool


class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        self._tools [
            tool.definition.name
        ] = tool

    def get_tool(self, name: str) -> BaseTool:

        return self._tools [name]

    def get_tool_definitions(
            self,
    ) -> list:
        return [
            tool.definition
            for tool in self._tools.values()
        ]