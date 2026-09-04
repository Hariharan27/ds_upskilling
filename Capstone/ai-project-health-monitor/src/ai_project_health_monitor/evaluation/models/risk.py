from pydantic import BaseModel, Field

from ai_project_health_monitor.domain.models.risk_signal import (
    RiskSeverity,
    RiskType,
)


class RiskEvaluationCase(BaseModel):
    """Expected risk detection for a project evidence set."""

    case_id: str = Field(min_length=1)
    project_id: str = Field(min_length=1)
    evidence_event_ids: list[str] = Field(min_length=1)
    expected_risk_types: list[RiskType] = Field(default_factory=list)
    expected_severities: list[RiskSeverity] = Field(default_factory=list)
    expected_evidence_event_ids: list[str] = Field(default_factory=list)


class RiskEvaluationResult(BaseModel):
    """Evaluation result for one risk-analysis case."""

    case_id: str
    predicted_risk_types: list[RiskType]
    expected_risk_types: list[RiskType]
    predicted_severities: list[RiskSeverity]
    expected_severities: list[RiskSeverity]
    predicted_evidence_event_ids: list[str]
    expected_evidence_event_ids: list[str]
    true_positive_count: int = Field(ge=0)
    false_positive_count: int = Field(ge=0)
    false_negative_count: int = Field(ge=0)
    severity_correct: bool
    evidence_correct: bool


class RiskEvaluationSummary(BaseModel):
    """Aggregated risk-analysis evaluation metrics."""

    total_cases: int = Field(ge=0)
    true_positive_count: int = Field(ge=0)
    false_positive_count: int = Field(ge=0)
    false_negative_count: int = Field(ge=0)
    precision: float = Field(ge=0.0, le=1.0)
    recall: float = Field(ge=0.0, le=1.0)
    f1: float = Field(ge=0.0, le=1.0)
    severity_accuracy: float = Field(ge=0.0, le=1.0)
    evidence_accuracy: float = Field(ge=0.0, le=1.0)


class RiskEvaluationRun(BaseModel):
    """Complete evaluation run containing summary and case results."""

    summary: RiskEvaluationSummary
    results: list[RiskEvaluationResult]