import os
import threading
import time

import torch
from omnivoice import OmniVoice

from app.core.config import settings
from app.core.logger import logger

# --------------------------------------------------------
# Disable HF XET
# --------------------------------------------------------

os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

# --------------------------------------------------------
# Local model location
# --------------------------------------------------------

LOCAL_MODEL_PATH = "/content/drive/MyDrive/OmniVoice"


class ModelManager:

    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):

        if cls._instance is None:

            with cls._instance_lock:

                if cls._instance is None:

                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if getattr(self, "_initialized", False):
            return

        self._initialized = True

        self.model = None

        self.loaded = False

        self.loading = False

        self.load_lock = threading.Lock()

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.dtype = (
            torch.float16
            if self.device == "cuda"
            else torch.float32
        )

        self.sampling_rate = None

    # --------------------------------------------------------

    def initialize(self):

        if self.loaded:
            return

        with self.load_lock:

            if self.loaded:
                return

            self.loading = True

            logger.info("=" * 60)
            logger.info("Loading OmniVoice Model...")
            logger.info(f"Device : {self.device}")
            logger.info(f"Model Path : {LOCAL_MODEL_PATH}")

            start = time.perf_counter()

            try:

                if not os.path.exists(LOCAL_MODEL_PATH):

                    raise FileNotFoundError(
                        f"Model folder not found:\n{LOCAL_MODEL_PATH}"
                    )

                self.model = OmniVoice.from_pretrained(
                    LOCAL_MODEL_PATH,
                    device_map=self.device,
                    torch_dtype=self.dtype,
                    load_asr=settings.LOAD_ASR,
                )

                self.sampling_rate = self.model.sampling_rate

                self.loaded = True

                elapsed = time.perf_counter() - start

                logger.success("Model loaded successfully.")
                logger.info(f"Sampling Rate : {self.sampling_rate}")
                logger.info(f"Load Time : {elapsed:.2f} sec")

            except Exception as e:

                logger.exception(e)
                raise

            finally:

                self.loading = False

    # --------------------------------------------------------

    def get_model(self):

        self.initialize()

        return self.model

    # --------------------------------------------------------

    def health(self):

        return {
            "status": "ready" if self.loaded else "loading",
            "gpu": torch.cuda.is_available(),
            "device": self.device,
            "sampling_rate": self.sampling_rate,
        }


model_manager = ModelManager()
