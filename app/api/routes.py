from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/")
async def root():

    return {
        "message": "Welcome to OmniVoice Server"
    }


@router.get("/health")
async def health():

    return {
        "status": "online",
        "server": settings.APP_NAME,
        "version": settings.VERSION,
    }