from fastapi import FastAPI

from backend.app.api.v1.chat import router as chat_router
from backend.app.api.v1.health import router as health_router
from backend.app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(health_router)
app.include_router(chat_router, prefix="/api/v1")