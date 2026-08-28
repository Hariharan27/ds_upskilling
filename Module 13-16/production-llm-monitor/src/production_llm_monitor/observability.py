import json
import logging
import sys
import traceback
from typing import Any
from uuid import uuid4


logger = logging.getLogger("production_llm_monitor")


def configure_logging() -> None:
    """Configure structured JSON logging."""

    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(
        logging.Formatter("%(message)s")
    )

    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)


def log_event(
    event: str,
    **fields: Any,
) -> None:
    """Write a structured JSON log event."""

    payload = {
        "event": event,
        **fields,
    }

    logger.info(json.dumps(payload, default=str))


def create_correlation_id() -> str:
    """Create a unique ID for one application request."""

    return str(uuid4())


def log_error(
    error: Exception,
    *,
    correlation_id: str,
    model: str,
) -> None:
    """Record a structured error event."""

    log_event(
        "llm_request_failed",
        correlation_id=correlation_id,
        model=model,
        error_type=type(error).__name__,
        error_message=str(error),
        traceback=traceback.format_exc(),
    )