from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.engine import OmniVoiceEngine
from app.models import CloneRequest, CloneResponse
from app.services import VoiceService

router = APIRouter()

voice_service = VoiceService()
engine = OmniVoiceEngine()

# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@router.get("/health")
def health():

    return engine.health()


# ---------------------------------------------------------
# Clone
# ---------------------------------------------------------

@router.post(
    "/clone",
    response_model=CloneResponse,
)
def clone(request: CloneRequest):

    try:

        return voice_service.clone(request)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------------------
# Download Generated Audio
# ---------------------------------------------------------

@router.get("/download/{filename}")
def download(filename: str):

    # Prevent path traversal attacks
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