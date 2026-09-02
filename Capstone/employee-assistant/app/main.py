import logging
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.request_context import (
    create_request_id,
    request_id_context,
)

from app.api.routes.chat import router as chat_router
from app.core.exceptions import OutputValidationError

configure_logging()

logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version,
)

app.include_router(chat_router)


@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next,
):
    request_id = create_request_id()

    request_id_context.set(request_id)

    start_time = perf_counter()

    logger.info(
        "request_started request_id=%s method=%s path=%s",
        request_id,
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    duration_ms = (perf_counter() - start_time) * 1000

    logger.info(
        "request_completed request_id=%s status=%s duration_ms=%.2f",
        request_id,
        response.status_code,
        duration_ms,
    )

    response.headers["X-Request-ID"] = request_id

    return response


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.exception_handler(OutputValidationError)
async def output_validation_exception_handler(
    request: Request,
    exc: OutputValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": (
                "I couldn't generate a reliable answer for your request. "
                "Please try rephrasing it."
            )
        },
    )