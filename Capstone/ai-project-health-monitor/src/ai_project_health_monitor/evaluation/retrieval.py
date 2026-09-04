from collections.abc import Callable, Sequence

from ai_project_health_monitor.evaluation.models.retrieval import (
    RetrievalEvaluationCase,
    RetrievalEvaluationResult,
    RetrievalEvaluationSummary,
)
from ai_project_health_monitor.rag.models.retrieval import RetrievalResult


class RetrievalEvaluator:
    """Evaluate retrieval quality against a golden dataset."""

    def __init__(
        self,
        retrieve: Callable[
            [str, str, int],
            Sequence[RetrievalResult],
        ],
    ) -> None:
        self._retrieve = retrieve

    def evaluate_case(
        self,
        case: RetrievalEvaluationCase,
        k: int,
    ) -> RetrievalEvaluationResult:
        """Evaluate one retrieval case."""
        if k <= 0:
            raise ValueError("k must be greater than zero")

        results = self._retrieve(
            case.query,
            case.project_id,
            k,
        )

        retrieved_event_ids = [
            result.chunk.event_id
            for result in results
        ]

        relevant_event_ids = set(case.relevant_event_ids)
        retrieved_event_id_set = set(retrieved_event_ids)

        relevant_retrieved_count = len(
            retrieved_event_id_set & relevant_event_ids
        )

        precision_at_k = (
            relevant_retrieved_count / len(retrieved_event_ids)
            if retrieved_event_ids
            else 0.0
        )

        recall_at_k = (
            relevant_retrieved_count / len(relevant_event_ids)
            if relevant_event_ids
            else None
        )

        false_positive_count = (
            len(retrieved_event_id_set)
            if not relevant_event_ids
            else len(
                retrieved_event_id_set - relevant_event_ids
            )
        )

        cross_project_results = [
            result.chunk.event_id
            for result in results
            if result.chunk.project_id != case.project_id
        ]

        return RetrievalEvaluationResult(
            query_id=case.query_id,
            retrieved_event_ids=retrieved_event_ids,
            relevant_event_ids=case.relevant_event_ids,
            hit=(
                relevant_retrieved_count > 0
                if relevant_event_ids
                else len(retrieved_event_ids) == 0
            ),            precision_at_k=precision_at_k,
            recall_at_k=recall_at_k,
            false_positive_count=false_positive_count,
            cross_project_results=cross_project_results,
        )

    def evaluate(
        self,
        cases: Sequence[RetrievalEvaluationCase],
        k: int,
    ) -> RetrievalEvaluationSummary:
        """Evaluate all golden cases and aggregate metrics."""
        if k <= 0:
            raise ValueError("k must be greater than zero")

        if not cases:
            return RetrievalEvaluationSummary(
                total_cases=0,
                hit_rate=0.0,
                mean_precision_at_k=0.0,
                mean_recall_at_k=None,
                cross_project_result_count=0,
                negative_cases=0,
                negative_false_positive_cases=0,
            )

        results = [
            self.evaluate_case(case, k)
            for case in cases
        ]

        recall_values = [
            result.recall_at_k
            for result in results
            if result.recall_at_k is not None
        ]

        negative_results = [
            result
            for case, result in zip(cases, results, strict=True)
            if not case.relevant_event_ids
        ]

        positive_results = [
            result
            for case, result in zip(cases, results, strict=True)
            if case.relevant_event_ids
        ]

        return RetrievalEvaluationSummary(
            total_cases=len(results),
            hit_rate=(
                sum(result.hit for result in positive_results)
                / len(positive_results)
                if positive_results
                else 0.0
            ),
            mean_precision_at_k=(
                sum(result.precision_at_k for result in results)
                / len(results)
            ),
            mean_recall_at_k=(
                sum(recall_values) / len(recall_values)
                if recall_values
                else None
            ),
            cross_project_result_count=sum(
                len(result.cross_project_results)
                for result in results
            ),
            negative_cases=len(negative_results),
            negative_false_positive_cases=sum(
                result.false_positive_count > 0
                for result in negative_results
            ),
        )