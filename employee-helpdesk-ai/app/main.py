from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.tickets import router as ticket_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)


app.include_router(
    ticket_router,
    prefix="/api/v1",
    tags=["Tickets"]
)
