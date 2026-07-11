from fastapi import APIRouter, HTTPException

from app.models import CloneRequest, CloneResponse
from app.services import VoiceService
from app.engine import OmniVoiceEngine

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
def clone(
    request: CloneRequest,
):

    try:

        return voice_service.clone(request)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )