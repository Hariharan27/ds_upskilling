from app.application.services.rag.models import (
    RAGRequest,
)
from app.application.services.rag.rag_generation_service import (
    RAGGenerationService,
)
from app.domain.models.tool_definition import (
    ToolDefinition,
)
from app.domain.models.tool_execution_request import (
    ToolExecutionRequest,
)
from app.domain.models.tool_execution_result import (
    ToolExecutionResult,
)
from app.domain.tools.base_tool import (
    BaseTool,
)


class SearchDocumentsTool(BaseTool):

    def __init__(
        self,
        rag_generation_service: RAGGenerationService,
    ) -> None:

        self._rag_generation_service = rag_generation_service

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

        rag_request = RAGRequest(
            query=request.query,
            conversation_history=request.conversation_history,
        )

        rag_response = self._rag_generation_service.generate(
            rag_request,
        )

        return ToolExecutionResult(
            success=True,
            data={
                "answer": rag_response.answer,
                "sources": rag_response.sources,
                "input_tokens": rag_response.input_tokens,
                "output_tokens": rag_response.output_tokens,
                "total_tokens": rag_response.total_tokens,
            },
        )