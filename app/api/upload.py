import os
import tempfile

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
)

from app.models import (
    ApiResponse,
    CloneRequest,
    CloneResponse,
)
from app.services import VoiceService

router = APIRouter()

voice_service = VoiceService()


# ==========================================================
# Clone Voice (Desktop Upload API)
# ==========================================================

@router.post(
    "/clone-upload",
    response_model=ApiResponse,
)
async def clone_upload(

    text: str = Form(...),

    language: str = Form("English"),

    reference_audio: UploadFile = File(...),

):

    suffix = os.path.splitext(
        reference_audio.filename
    )[1]

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    )

    try:

        temp_file.write(
            await reference_audio.read()
        )

        temp_file.close()

        request = CloneRequest(

            text=text,

            language=language,

            reference_audio=temp_file.name,

        )

        result: CloneResponse = voice_service.clone(
            request
        )

        return ApiResponse(

            success=True,

            message="Voice generated successfully.",

            data=result.model_dump(),

        )

    finally:

        if os.path.exists(temp_file.name):

            os.remove(temp_file.name)