from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.shared.config import get_settings
from app.presentation.api.routes.health import router as health_router
from app.presentation.api.routes import (
    chat,
)

settings = get_settings()


app = FastAPI(
    title="iBuddy",
    description="The Ideator's Workplace Knowledge Companion",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(health_router)
app.include_router(
    chat.router,
)