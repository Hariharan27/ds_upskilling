from datetime import UTC, datetime

from ai_project_health_monitor.analysis.risk_grounding_validator import (
    DeterministicRiskGroundingValidator,
)
from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.domain.models.project_event import SourceType
from ai_project_health_monitor.domain.models.risk_signal import (
    RiskSeverity,
    RiskSignal,
    RiskType,
)


def test_scope_creep_accepts_additional_requested_requirement() -> None:
    evidence = Evidence(
        event_id="EVT-EMAIL-002",
        source_type=SourceType.EMAIL,
        source_id="EMAIL-002",
        content=(
            "We would also like to include an additional reporting "
            "dashboard in the current release."
        ),
        occurred_at=datetime(
            2026,
            9,
            3,
            9,
            15,
            tzinfo=UTC,
        ),
    )

    risk = RiskSignal(
        signal_id="RISK-TEST-001",
        project_id="PROJ-001",
        event_id=evidence.event_id,
        risk_type=RiskType.SCOPE_CREEP,
        severity=RiskSeverity.MEDIUM,
        confidence=0.95,
        evidence=evidence,
        evidence_quote=(
            "include an additional reporting dashboard "
            "in the current release"
        ),
        rationale=(
            "An additional reporting requirement has been requested."
        ),
    )

    validator = DeterministicRiskGroundingValidator()

    validator.validate(
        risk=risk,
        evidence=evidence,
    )