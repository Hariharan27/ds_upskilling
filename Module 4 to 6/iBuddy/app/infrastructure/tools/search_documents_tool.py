from app.application.services.retrieval.multi_query_retrieval_service import MultiQueryRetrievalService
from app.domain.entities.retrieval_request import RetrievalRequest
from app.domain.models.tool_definition import (
    ToolDefinition,
)
from app.domain.models.tool_execution_request import (
    ToolExecutionRequest,
)
from app.domain.models.tool_execution_result import (
    ToolExecutionResult,
)
from app.domain.services.context_builder import ContextBuilder
from app.domain.tools.base_tool import (
    BaseTool,
)


class SearchDocumentsTool(BaseTool):

    def __init__(
        self,
        retrieval_service: MultiQueryRetrievalService,
        context_builder: ContextBuilder,
    ) -> None:

        self._retrieval_service = retrieval_service
        self._context_builder = context_builder

    @property
    def definition(
        self,
    ) -> ToolDefinition:

        return ToolDefinition(
        name="search_documents",
        description= (
        "Search the enterprise knowledge base for company policies, "
        "HR policies, WFH policies, leave policies, engineering "
        "documentation, onboarding guides, process documents, and "
        "other organizational knowledge. "
        "Use this tool only for questions whose answers are expected "
        "to be found in enterprise documentation. "
        "Do NOT use this tool for employee-specific or personalized "
        "information such as leave balance, attendance, payroll, "
        "employee profile, holiday balance, or any information that "
        "requires accessing employee records."
    ),
)

    def execute(
            self,
            request: ToolExecutionRequest,
    ) -> ToolExecutionResult:
        retrieval_request = RetrievalRequest(
            query=request.query,
            conversation_history=request.conversation_history,
        )

        results = self._retrieval_service.retrieve(
            retrieval_request,
        )

        context = self._context_builder.build(
            results,
        )

        sources = sorted(
            {
                result.file_name
                for result in results
            }
        )

        return ToolExecutionResult(
            success=True,
            context=context,
            sources=sources,
            data={
                "results": results,
            },
        )