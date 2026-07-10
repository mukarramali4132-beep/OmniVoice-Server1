import threading
import time

import soundfile as sf
import torch

from app.core.config import settings
from app.core.logger import logger
from app.engine.model_manager import ModelManager
from app.utils.uuid import uuid_filename


class OmniVoiceEngine:
    """
    Production OmniVoice Engine.
    Responsible only for voice generation.
    """

    def __init__(self):

        self.manager = ModelManager()

        self.generate_lock = threading.Lock()

    # ---------------------------------------------------------

    def health(self):

        return self.manager.health()

    # ---------------------------------------------------------

    def clone(
        self,
        *,
        text: str,
        reference_audio: str,
        language: str | None = None,
        reference_text: str | None = None,
        speed: float | None = None,
        duration: float | None = None,
    ) -> dict:

        model = self.manager.get_model()

        with self.generate_lock:

            start = time.perf_counter()

            logger.info("Creating voice clone prompt...")

            prompt = model.create_voice_clone_prompt(
                ref_audio=reference_audio,
                ref_text=reference_text,
                preprocess_prompt=True,
            )

            logger.info("Generating speech...")

            audio = model.generate(
                text=text,
                language=language,
                voice_clone_prompt=prompt,
                speed=speed,
                duration=duration,
            )

            if not audio:
                raise RuntimeError(
                    "OmniVoice returned empty audio."
                )

            waveform = audio[0]

            if torch.is_tensor(waveform):

                waveform = (
                    waveform
                    .detach()
                    .cpu()
                    .numpy()
                )

            filename = uuid_filename()

            output_path = (
                settings.AUDIO_DIR / filename
            )

            sf.write(
                str(output_path),
                waveform,
                self.manager.sampling_rate,
            )

            elapsed = (
                time.perf_counter() - start
            )

            logger.success(
                f"Voice generated in {elapsed:.2f} sec"
            )

            return {

                "success": True,

                "filename": filename,

                "path": str(output_path),

                "duration":
                    len(waveform)
                    / self.manager.sampling_rate,

                "sampling_rate":
                    self.manager.sampling_rate,
            }