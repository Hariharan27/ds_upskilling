from abc import ABC, abstractmethod

from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.domain.models.risk_signal import RiskSignal


class RiskAnalyzer(ABC):
    """Contract for extracting risk signals from project evidence."""

    @abstractmethod
    def analyze(
        self,
        project_id: str,
        evidence: list[Evidence],
    ) -> list[RiskSignal]:
        """Analyze project evidence and return detected risk signals."""
        raise NotImplementedError