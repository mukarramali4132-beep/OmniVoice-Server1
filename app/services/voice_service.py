from pathlib import Path

from app.core.errors import (
    GenerationFailedError,
    ModelNotLoadedError,
    ReferenceAudioNotFoundError,
)
from app.core.logger import logger
from app.engine import OmniVoiceEngine
from app.models import CloneRequest, CloneResponse


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

        # -----------------------------------------------------
        # Validate reference audio
        # -----------------------------------------------------

        if not Path(request.reference_audio).exists():

            raise ReferenceAudioNotFoundError(
                request.reference_audio
            )

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

        except ReferenceAudioNotFoundError:
            raise

        except RuntimeError as e:

            raise GenerationFailedError(
                str(e)
            ) from e

        except AttributeError as e:

            raise ModelNotLoadedError() from e

        except Exception as e:

            logger.exception(e)

            raise GenerationFailedError(
                "Unexpected error during voice generation."
            ) from e