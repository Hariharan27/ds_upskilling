from ai_project_health_monitor.domain.models.risk_change import (
    RiskChange,
    RiskChangeType,
)
from ai_project_health_monitor.domain.models.risk_signal import RiskSignal


class RiskStateReconciler:
    """Build a stable current risk state from detected risk changes."""

    def reconcile(
        self,
        previous_risks: list[RiskSignal],
        current_risks: list[RiskSignal],
        risk_changes: list[RiskChange],
    ) -> list[RiskSignal]:
        """Reconcile current risks using the detected risk evolution."""
        current_by_id = {
            risk.signal_id: risk
            for risk in current_risks
        }

        reconciled: list[RiskSignal] = []

        for change in risk_changes:
            if change.change_type == RiskChangeType.RESOLVED:
                continue

            if change.current_risk is None:
                continue

            current_risk = current_by_id.get(
                change.current_risk.signal_id
            )

            if current_risk is None:
                continue

            if change.change_type == RiskChangeType.CONTINUING:
                if change.previous_risk is None:
                    reconciled.append(current_risk)
                    continue

                reconciled.append(
                    current_risk.model_copy(
                        update={
                            "severity": change.previous_risk.severity,
                        }
                    )
                )
                continue

            reconciled.append(current_risk)

        return reconciled