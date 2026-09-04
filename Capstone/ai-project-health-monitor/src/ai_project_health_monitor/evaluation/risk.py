from collections.abc import Callable, Sequence

from ai_project_health_monitor.domain.models.evidence import Evidence
from ai_project_health_monitor.domain.models.risk_signal import RiskSignal
from ai_project_health_monitor.evaluation.models.risk import (
    RiskEvaluationCase,
    RiskEvaluationResult,
    RiskEvaluationRun,
    RiskEvaluationSummary,
)


class RiskEvaluator:
    """Evaluate risk detection against a golden dataset."""

    def __init__(
        self,
        analyze: Callable[
            [str, list[Evidence]],
            Sequence[RiskSignal],
        ],
    ) -> None:
        self._analyze = analyze

    def evaluate_case(
        self,
        case: RiskEvaluationCase,
        evidence: list[Evidence],
    ) -> RiskEvaluationResult:
        """Evaluate one risk-analysis case."""
        predicted_signals = self._analyze(
            case.project_id,
            evidence,
        )

        predicted_types = [
            signal.risk_type
            for signal in predicted_signals
        ]

        expected_types = case.expected_risk_types

        predicted_type_set = set(predicted_types)
        expected_type_set = set(expected_types)

        true_positive_count = len(
            predicted_type_set & expected_type_set
        )

        false_positive_count = len(
            predicted_type_set - expected_type_set
        )

        false_negative_count = len(
            expected_type_set - predicted_type_set
        )

        predicted_evidence_event_ids = [
            signal.event_id
            for signal in predicted_signals
        ]

        expected_evidence_event_ids = (
            case.expected_evidence_event_ids
        )

        severity_correct = (
            [signal.severity for signal in predicted_signals]
            == case.expected_severities
        )

        evidence_correct = (
            sorted(set(predicted_evidence_event_ids))
            == sorted(set(expected_evidence_event_ids))
        )

        return RiskEvaluationResult(
            case_id=case.case_id,
            predicted_risk_types=predicted_types,
            expected_risk_types=expected_types,
            predicted_severities=[
                signal.severity
                for signal in predicted_signals
            ],
            expected_severities=case.expected_severities,
            predicted_evidence_event_ids=predicted_evidence_event_ids,
            expected_evidence_event_ids=expected_evidence_event_ids,
            true_positive_count=true_positive_count,
            false_positive_count=false_positive_count,
            false_negative_count=false_negative_count,
            severity_correct=severity_correct,
            evidence_correct=evidence_correct,
        )

    def evaluate(
        self,
        cases: Sequence[RiskEvaluationCase],
        evidence_by_case: dict[str, list[Evidence]],
    ) -> RiskEvaluationRun:
        """Evaluate all risk-analysis cases."""
        if not cases:
            return RiskEvaluationRun(
                summary=RiskEvaluationSummary(
                    total_cases=0,
                    true_positive_count=0,
                    false_positive_count=0,
                    false_negative_count=0,
                    precision=0.0,
                    recall=0.0,
                    f1=0.0,
                    severity_accuracy=0.0,
                    evidence_accuracy=0.0,
                ),
                results=[],
            )

        results = [
            self.evaluate_case(
                case,
                evidence_by_case[case.case_id],
            )
            for case in cases
        ]

        true_positive_count = sum(
            result.true_positive_count
            for result in results
        )

        false_positive_count = sum(
            result.false_positive_count
            for result in results
        )

        false_negative_count = sum(
            result.false_negative_count
            for result in results
        )

        precision_denominator = (
            true_positive_count + false_positive_count
        )

        recall_denominator = (
            true_positive_count + false_negative_count
        )

        precision = (
            true_positive_count / precision_denominator
            if precision_denominator
            else 0.0
        )

        recall = (
            true_positive_count / recall_denominator
            if recall_denominator
            else 0.0
        )

        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )

        severity_accuracy = (
            sum(result.severity_correct for result in results)
            / len(results)
        )

        evidence_accuracy = (
            sum(result.evidence_correct for result in results)
            / len(results)
        )

        return RiskEvaluationRun(
            summary=RiskEvaluationSummary(
                total_cases=len(results),
                true_positive_count=true_positive_count,
                false_positive_count=false_positive_count,
                false_negative_count=false_negative_count,
                precision=precision,
                recall=recall,
                f1=f1,
                severity_accuracy=severity_accuracy,
                evidence_accuracy=evidence_accuracy,
            ),
            results=results,
        )