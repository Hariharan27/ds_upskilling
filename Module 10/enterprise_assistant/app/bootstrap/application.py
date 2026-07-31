from fastapi import FastAPI

from app.presentation.api.routes.health import router as health_router
from app.shared.config import Settings, get_settings


def create_application(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""

    application_settings = settings or get_settings()

    application = FastAPI(
        title=application_settings.app_name,
        version=application_settings.app_version,
        debug=application_settings.debug,
    )

    application.include_router(health_router)

    return application


app = create_application()