from datetime import UTC, datetime
from unittest.mock import Mock

from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.domain.models.risk_change import (
    RiskChange,
    RiskChangeType,
)
from ai_project_health_monitor.domain.models.risk_signal import (
    RiskSeverity,
    RiskSignal,
    RiskType,
)
from ai_project_health_monitor.orchestration.nodes.reconcile_risk_state import (
    ReconcileRiskStateNode,
)
from ai_project_health_monitor.orchestration.state import ProjectHealthState


def build_risk(
    signal_id: str,
    risk_type: RiskType,
    severity: RiskSeverity,
) -> RiskSignal:
    evidence = Evidence(
        event_id=f"EVENT-{signal_id}",
        source_type="jira",
        source_id=f"SOURCE-{signal_id}",
        content="Test evidence",
        occurred_at=datetime.now(UTC),
    )

    return RiskSignal(
        signal_id=signal_id,
        project_id="PROJ-001",
        event_id=evidence.event_id,
        risk_type=risk_type,
        severity=severity,
        confidence=0.95,
        evidence=evidence,
        evidence_quote="Test evidence",
        rationale="Test rationale",
    )


def test_reconcile_risk_state_node_updates_risk_signals() -> None:
    previous = build_risk(
        "previous-1",
        RiskType.CLIENT_SENTIMENT,
        RiskSeverity.MEDIUM,
    )
    current = build_risk(
        "current-1",
        RiskType.CLIENT_SENTIMENT,
        RiskSeverity.HIGH,
    )

    change = RiskChange(
        project_id="PROJ-001",
        change_type=RiskChangeType.CONTINUING,
        previous_risk=previous,
        current_risk=current,
        rationale="Same underlying risk continues.",
    )

    reconciler = Mock()
    reconciler.reconcile.return_value = [
        current.model_copy(
            update={"severity": RiskSeverity.MEDIUM}
        )
    ]

    node = ReconcileRiskStateNode(
        risk_state_reconciler=reconciler,
    )

    state = ProjectHealthState(
        project_id="PROJ-001",
        query="project health assessment",
        risk_signals=[current],
        risk_changes=[change],
    )

    result = node(state)

    reconciler.reconcile.assert_called_once()
    assert result["risk_signals"][0].signal_id == "current-1"
    assert result["risk_signals"][0].severity == RiskSeverity.MEDIUM