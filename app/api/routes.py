from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.engine import OmniVoiceEngine
from app.models import (
    ApiResponse,
    CloneRequest,
    CloneResponse,
)
from app.services import VoiceService

router = APIRouter()

voice_service = VoiceService()
engine = OmniVoiceEngine()


# ==========================================================
# Health
# ==========================================================

@router.get(
    "/health",
    response_model=ApiResponse,
)
def health():

    return ApiResponse(
        success=True,
        message="Server is ready.",
        data=engine.health(),
    )


# ==========================================================
# Clone Voice
# ==========================================================

@router.post(
    "/clone",
    response_model=ApiResponse,
)
def clone(
    request: CloneRequest,
):

    result: CloneResponse = voice_service.clone(request)

    return ApiResponse(
        success=True,
        message="Voice generated successfully.",
        data=result.model_dump(),
    )


# ==========================================================
# Download Generated Audio
# ==========================================================

@router.get("/download/{filename}")
def download(
    filename: str,
):

    # Prevent path traversal
    filename = Path(filename).name

    file_path = settings.AUDIO_DIR / filename

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Audio file not found.",
        )

    return FileResponse(
        path=file_path,
        media_type="audio/wav",
        filename=filename,
    )