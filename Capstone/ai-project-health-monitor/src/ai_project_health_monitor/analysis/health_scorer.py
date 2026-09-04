from abc import ABC, abstractmethod

from ai_project_health_monitor.domain.models.health_score import HealthScore
from ai_project_health_monitor.domain.models.risk_signal import RiskSignal


class HealthScorer(ABC):
    """Contract for calculating deterministic project health scores."""

    @abstractmethod
    def calculate(
        self,
        project_id: str,
        risk_signals: list[RiskSignal],
    ) -> HealthScore:
        """Calculate the overall health score from risk signals."""
        raise NotImplementedError