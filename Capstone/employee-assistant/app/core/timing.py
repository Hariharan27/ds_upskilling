import logging
from contextlib import contextmanager
from time import perf_counter
from typing import Iterator

from app.core.request_context import get_request_id


logger = logging.getLogger(__name__)


@contextmanager
def log_duration(stage: str) -> Iterator[None]:
    start = perf_counter()

    try:
        yield
    finally:
        duration_ms = (perf_counter() - start) * 1000
        request_id = get_request_id()

        logger.info(
            "stage_completed request_id=%s stage=%s duration_ms=%.2f",
            request_id,
            stage,
            duration_ms,
        )