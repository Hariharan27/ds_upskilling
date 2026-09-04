from datetime import UTC, datetime

from ai_project_health_monitor.analysis.health_scorer import HealthScorer
from ai_project_health_monitor.domain.models.health_score import (
    HealthScore,
    HealthStatus,
)
from ai_project_health_monitor.domain.models.risk_signal import (
    RiskSeverity,
    RiskSignal,
)


class DeterministicHealthScorer(HealthScorer):
    """Calculate explainable project health scores from risk signals."""

    SEVERITY_PENALTIES: dict[RiskSeverity, float] = {
        RiskSeverity.LOW: 5.0,
        RiskSeverity.MEDIUM: 10.0,
        RiskSeverity.HIGH: 20.0,
        RiskSeverity.CRITICAL: 35.0,
    }

    AT_RISK_THRESHOLD = 70.0
    CRITICAL_THRESHOLD = 40.0

    def calculate(
        self,
        project_id: str,
        risk_signals: list[RiskSignal],
    ) -> HealthScore:
        """Calculate a deterministic health score from risk signals."""
        if not project_id.strip():
            raise ValueError("project_id cannot be empty")

        penalty = sum(
            self.SEVERITY_PENALTIES[signal.severity]
            * signal.confidence
            for signal in risk_signals
        )

        score = max(0.0, 100.0 - penalty)
        status = self._calculate_status(score)

        contributing_risks = [
            signal.signal_id
            for signal in risk_signals
        ]

        rationale = self._build_rationale(
            score=score,
            status=status,
            risk_signals=risk_signals,
        )

        return HealthScore(
            project_id=project_id,
            score=score,
            status=status,
            contributing_risks=contributing_risks,
            calculated_at=datetime.now(UTC),
            rationale=rationale,
        )

    def _calculate_status(self, score: float) -> HealthStatus:
        if score < self.CRITICAL_THRESHOLD:
            return HealthStatus.CRITICAL

        if score < self.AT_RISK_THRESHOLD:
            return HealthStatus.AT_RISK

        return HealthStatus.HEALTHY

    def _build_rationale(
        self,
        score: float,
        status: HealthStatus,
        risk_signals: list[RiskSignal],
    ) -> str:
        if not risk_signals:
            return (
                f"Project health score is {score:.1f}/100 "
                "with no detected risks."
            )

        risk_summary = ", ".join(
            f"{signal.risk_type.value} ({signal.severity.value})"
            for signal in risk_signals
        )

        return (
            f"Project health score is {score:.1f}/100 "
            f"and classified as {status.value}. "
            f"Contributing risks: {risk_summary}."
        )