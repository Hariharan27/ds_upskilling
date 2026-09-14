from ai_project_health_monitor.analysis.risk_state_reconciler import (
    RiskStateReconciler,
)
from ai_project_health_monitor.orchestration.state import ProjectHealthState


class ReconcileRiskStateNode:
    """LangGraph node responsible for stabilizing the current risk state."""

    def __init__(
        self,
        risk_state_reconciler: RiskStateReconciler,
    ) -> None:
        self._risk_state_reconciler = risk_state_reconciler

    def __call__(self, state: ProjectHealthState) -> dict[str, object]:
        reconciled_risks = self._risk_state_reconciler.reconcile(
            previous_risks=(
                state.previous_health_snapshot.risk_signals
                if state.previous_health_snapshot is not None
                else []
            ),
            current_risks=state.risk_signals,
            risk_changes=state.risk_changes,
        )

        return {
            "risk_signals": reconciled_risks,
        }