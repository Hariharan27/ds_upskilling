from fastapi import FastAPI

from app.presentation.api.routes.health import router as health_router
from app.presentation.api.routes import (
    chat,
)

app = FastAPI(
    title="iBuddy",
    description="The Ideator's Workplace Knowledge Companion",
    version="1.0.0",
)



app.include_router(health_router)
app.include_router(
    chat.router,
)