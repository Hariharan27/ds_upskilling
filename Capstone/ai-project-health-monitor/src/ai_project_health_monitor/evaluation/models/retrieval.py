from pydantic import BaseModel, Field


class RetrievalEvaluationCase(BaseModel):
    """Golden test case for evaluating retrieval quality."""

    query_id: str = Field(min_length=1)
    query: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    relevant_event_ids: list[str]


class RetrievalEvaluationResult(BaseModel):
    """Evaluation result for a single retrieval query."""

    query_id: str = Field(min_length=1)
    retrieved_event_ids: list[str]
    relevant_event_ids: list[str]
    hit: bool
    precision_at_k: float = Field(ge=0.0, le=1.0)
    recall_at_k: float | None = Field(default=None, ge=0.0, le=1.0)
    false_positive_count: int = Field(ge=0)
    cross_project_results: list[str] = Field(default_factory=list)


class RetrievalEvaluationSummary(BaseModel):
    """Aggregated retrieval evaluation metrics."""

    total_cases: int = Field(ge=0)
    hit_rate: float = Field(ge=0.0, le=1.0)
    mean_precision_at_k: float = Field(ge=0.0, le=1.0)
    mean_recall_at_k: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
    cross_project_result_count: int = Field(ge=0)
    negative_cases: int = Field(ge=0)
    negative_false_positive_cases: int = Field(ge=0)