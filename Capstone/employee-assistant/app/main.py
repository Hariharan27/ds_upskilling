from fastapi import FastAPI
from app.core.config import get_settings

from app.api.routes.chat import router as chat_router


settings = get_settings()


app = FastAPI(
    title= settings.app_name,
    description=settings.description,
    version=settings.app_version,
)

app.include_router(chat_router)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

