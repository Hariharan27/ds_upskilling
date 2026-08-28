import time
from langfuse import get_client, observe
from dotenv import load_dotenv

from production_llm_monitor.llm import LLMClient
from production_llm_monitor.observability import (
    configure_logging,
    create_correlation_id,
    log_event,
)
from production_llm_monitor.cost import calculate_cost
from production_llm_monitor.observability import (
    configure_logging,
    create_correlation_id,
    log_error,
    log_event,
)
from production_llm_monitor.evaluation import BasicEvaluator, Evaluator
from production_llm_monitor.guardrails import (
    GuardrailViolation,
    InputGuardrail,
    OutputGuardrail,
)

load_dotenv()

class LLMApplication:
    """Application layer for our LLM system."""

    def __init__(self, evaluator: Evaluator | None = None):
        configure_logging()
        self.llm = LLMClient()
        self.evaluator = evaluator or BasicEvaluator()
        self.input_guardrail = InputGuardrail()
        self.output_guardrail = OutputGuardrail()

    @observe()
    def ask(self,
            prompt: str,
            user_id: str | None = None,
            session_id: str | None = None,
            ) -> str:
        """Send a prompt to the LLM and monitor the request."""

        try:
            self.input_guardrail.validate(prompt)
        except GuardrailViolation as exc:
            log_event(
                "guardrail_blocked",
                reason=str(exc),
                user_id=user_id,
                session_id=session_id,
            )
            raise

        correlation_id = create_correlation_id()

        langfuse = get_client()

        langfuse.update_current_span(
            metadata={
                "correlation_id": correlation_id,
                "user_id": user_id,
                "session_id": session_id,
            }
        )

        log_event(
            "llm_request_started",
            correlation_id=correlation_id,
            model=self.llm.model,
        )

        start_time = time.perf_counter()

        try:

            result = self.llm.generate(prompt)

            response = result["content"]

            try:
                self.output_guardrail.validate(response)
            except GuardrailViolation as exc:
                log_event(
                    "guardrail_blocked",
                    reason=str(exc),
                    user_id=user_id,
                    session_id=session_id,
                )
                raise

            langfuse.update_current_span(
                metadata={
                    "cache_hit": result["cache_hit"],
                }
            )

            log_event(
                    "llm_cache_result",
                    correlation_id=correlation_id,
                    model=self.llm.model,
                    cache_hit=result["cache_hit"],
            )

            try:
                evaluation = self.evaluator.evaluate(prompt, response)

                langfuse.score_current_trace(
                    name="response_quality",
                    value=evaluation["score"],
                    data_type="NUMERIC",
                    comment=evaluation["label"],
                )

                log_event(
                    "llm_evaluation_completed",
                    correlation_id=correlation_id,
                    model=self.llm.model,
                    score=evaluation["score"],
                    label=evaluation["label"],
                )

            except Exception as exc:
                log_error(
                    exc,
                    correlation_id=correlation_id,
                    model=self.llm.model,
                )

                log_event(
                    "llm_evaluation_failed",
                    correlation_id=correlation_id,
                    model=self.llm.model,
                    error_type=type(exc).__name__,
                )

            cost = calculate_cost(
                model=self.llm.model,
                prompt_tokens=result["prompt_tokens"],
                completion_tokens=result["completion_tokens"],
            )

            latency_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            log_event(
                "llm_request_completed",
                correlation_id=correlation_id,
                model=self.llm.model,
                status="success",
                latency_ms=latency_ms,
                prompt_tokens=result["prompt_tokens"],
                completion_tokens=result["completion_tokens"],
                total_tokens=result["total_tokens"],
                estimated_cost_usd=cost,
            )

            return response

        except Exception as exc:
            latency_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            log_error(
                exc,
                correlation_id=correlation_id,
                model=self.llm.model,
            )

            log_event(
                "llm_request_failed",
                correlation_id=correlation_id,
                model=self.llm.model,
                status="error",
                latency_ms=latency_ms,
            )

            raise