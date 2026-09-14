from datetime import UTC, datetime

from ai_project_health_monitor.analysis.risk_state_reconciler import (
    RiskStateReconciler,
)
from ai_project_health_monitor.domain.models.risk_change import (
    RiskChange,
    RiskChangeType,
)
from ai_project_health_monitor.domain.models.risk_signal import (
    RiskSeverity,
    RiskSignal,
    RiskType,
)
from ai_project_health_monitor.domain.models.evidence import Evidence


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


def test_continuing_risk_preserves_previous_severity() -> None:
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
        rationale="Same underlying client sentiment issue continues.",
    )

    result = RiskStateReconciler().reconcile(
        previous_risks=[previous],
        current_risks=[current],
        risk_changes=[change],
    )

    assert len(result) == 1
    assert result[0].signal_id == "current-1"
    assert result[0].severity == RiskSeverity.MEDIUM


def test_resolved_risk_is_removed() -> None:
    previous = build_risk(
        "previous-1",
        RiskType.BLOCKER,
        RiskSeverity.HIGH,
    )

    change = RiskChange(
        project_id="PROJ-001",
        change_type=RiskChangeType.RESOLVED,
        previous_risk=previous,
        current_risk=None,
        rationale="Blocker is no longer supported by current evidence.",
    )

    result = RiskStateReconciler().reconcile(
        previous_risks=[previous],
        current_risks=[],
        risk_changes=[change],
    )

    assert result == []


def test_new_risk_uses_current_risk() -> None:
    current = build_risk(
        "current-1",
        RiskType.DELAY,
        RiskSeverity.HIGH,
    )

    change = RiskChange(
        project_id="PROJ-001",
        change_type=RiskChangeType.NEW,
        previous_risk=None,
        current_risk=current,
        rationale="New delay detected.",
    )

    result = RiskStateReconciler().reconcile(
        previous_risks=[],
        current_risks=[current],
        risk_changes=[change],
    )

    assert len(result) == 1
    assert result[0].signal_id == "current-1"
    assert result[0].severity == RiskSeverity.HIGH


def test_severity_increased_uses_current_severity() -> None:
    previous = build_risk(
        "previous-1",
        RiskType.DELAY,
        RiskSeverity.MEDIUM,
    )
    current = build_risk(
        "current-1",
        RiskType.DELAY,
        RiskSeverity.HIGH,
    )

    change = RiskChange(
        project_id="PROJ-001",
        change_type=RiskChangeType.SEVERITY_INCREASED,
        previous_risk=previous,
        current_risk=current,
        rationale="Evidence supports increased severity.",
    )

    result = RiskStateReconciler().reconcile(
        previous_risks=[previous],
        current_risks=[current],
        risk_changes=[change],
    )

    assert len(result) == 1
    assert result[0].severity == RiskSeverity.HIGH


def test_severity_decreased_uses_current_severity() -> None:
    previous = build_risk(
        "previous-1",
        RiskType.DELAY,
        RiskSeverity.HIGH,
    )
    current = build_risk(
        "current-1",
        RiskType.DELAY,
        RiskSeverity.MEDIUM,
    )

    change = RiskChange(
        project_id="PROJ-001",
        change_type=RiskChangeType.SEVERITY_DECREASED,
        previous_risk=previous,
        current_risk=current,
        rationale="Evidence supports decreased severity.",
    )

    result = RiskStateReconciler().reconcile(
        previous_risks=[previous],
        current_risks=[current],
        risk_changes=[change],
    )

    assert len(result) == 1
    assert result[0].severity == RiskSeverity.MEDIUM