from ai_project_health_monitor.analysis.evidence_adapter import EvidenceAdapter
from ai_project_health_monitor.analysis.health_scorer import HealthScorer
from ai_project_health_monitor.analysis.risk_analyzer import RiskAnalyzer
from ai_project_health_monitor.domain.models.health_score import HealthScore
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult


class ProjectHealthService:
    """Coordinate evidence retrieval, risk analysis, and health scoring."""

    def __init__(
        self,
        risk_analyzer: RiskAnalyzer,
        health_scorer: HealthScorer,
    ) -> None:
        self._risk_analyzer = risk_analyzer
        self._health_scorer = health_scorer

    def analyze(
        self,
        project_id: str,
        retrieval_results: list[RetrievalResult],
    ) -> HealthScore:
        """Analyze retrieved project evidence and calculate its health score."""
        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        evidence = EvidenceAdapter.from_retrieval_results(
            retrieval_results
        )

        risk_signals = self._risk_analyzer.analyze(
            project_id=project_id,
            evidence=evidence,
        )

        return self._health_scorer.calculate(
            project_id=project_id,
            risk_signals=risk_signals,
        )