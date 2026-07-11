from app.engine import OmniVoiceEngine
from app.models import CloneRequest, CloneResponse
from app.core.logger import logger


class VoiceService:
    """
    Business logic for voice cloning.
    """

    def __init__(self):

        self.engine = OmniVoiceEngine()

    # ---------------------------------------------------------

    def clone(
        self,
        request: CloneRequest,
    ) -> CloneResponse:

        logger.info("VoiceService: Clone request received.")

        try:

            result = self.engine.clone(

                text=request.text,

                language=request.language,

                reference_audio=request.reference_audio,

                reference_text=request.reference_text,

                speed=request.speed,

                duration=request.duration,

            )

            logger.success("Voice generated successfully.")

            return CloneResponse(**result)

        except Exception as e:

            logger.exception(e)

            raise