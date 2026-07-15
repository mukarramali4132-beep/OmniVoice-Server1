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


# Disable HF XET (optional but safe)
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"


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

<<<<<<< HEAD
    # --------------------------------------------------------
=======
    # ----------------------------------------------------------
>>>>>>> eee99e9 (Load OmniVoice model from local Drive and improve startup)

    def initialize(self):

        if self.loaded:
            return

        with self.load_lock:

            if self.loaded:
                return

            self.loading = True

            logger.info("=" * 60)
            logger.info("Loading OmniVoice Model...")
<<<<<<< HEAD
            logger.info(f"Device : {self.device}")
            logger.info(f"Model Path : {LOCAL_MODEL_PATH}")
=======
            logger.info(f"Device       : {self.device}")
            logger.info(f"Model Path   : {settings.MODEL_PATH}")
>>>>>>> eee99e9 (Load OmniVoice model from local Drive and improve startup)

            start = time.perf_counter()

            try:

<<<<<<< HEAD
                if not os.path.exists(LOCAL_MODEL_PATH):

                    raise FileNotFoundError(
                        f"Model folder not found:\n{LOCAL_MODEL_PATH}"
                    )

                self.model = OmniVoice.from_pretrained(
                    LOCAL_MODEL_PATH,
=======
                if not settings.MODEL_PATH.exists():

                    raise FileNotFoundError(
                        f"Model folder not found:\n{settings.MODEL_PATH}"
                    )

                self.model = OmniVoice.from_pretrained(
                    str(settings.MODEL_PATH),
>>>>>>> eee99e9 (Load OmniVoice model from local Drive and improve startup)
                    device_map=self.device,
                    torch_dtype=self.dtype,
                    load_asr=settings.LOAD_ASR,
                )

                self.sampling_rate = self.model.sampling_rate

                self.loaded = True

                elapsed = time.perf_counter() - start

                logger.success("Model loaded successfully.")
<<<<<<< HEAD
                logger.info(f"Sampling Rate : {self.sampling_rate}")
                logger.info(f"Load Time : {elapsed:.2f} sec")
=======
>>>>>>> eee99e9 (Load OmniVoice model from local Drive and improve startup)

            except Exception as e:

<<<<<<< HEAD
                logger.exception(e)
                raise
=======
                logger.info(
                    f"Load Time     : {elapsed:.2f} sec"
                )
>>>>>>> eee99e9 (Load OmniVoice model from local Drive and improve startup)

            except Exception as e:

                logger.exception(e)

                raise

            finally:

                self.loading = False

<<<<<<< HEAD
    # --------------------------------------------------------
=======
    # ----------------------------------------------------------
>>>>>>> eee99e9 (Load OmniVoice model from local Drive and improve startup)

    def get_model(self):

        self.initialize()

        return self.model

<<<<<<< HEAD
    # --------------------------------------------------------
=======
    # ----------------------------------------------------------

    def unload(self):

        if self.model is not None:

            del self.model

            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            self.model = None

            self.loaded = False

            logger.info("Model unloaded.")

    # ----------------------------------------------------------
>>>>>>> eee99e9 (Load OmniVoice model from local Drive and improve startup)

    def health(self):

        return {
            "status": "ready" if self.loaded else "loading",
            "gpu": torch.cuda.is_available(),
            "device": self.device,
            "sampling_rate": self.sampling_rate,
        }


<<<<<<< HEAD
model_manager = ModelManager()
=======
            "device":
                self.device,

            "gpu":
                torch.cuda.is_available(),

            "sampling_rate":
                self.sampling_rate,

            "loaded":
                self.loaded,

            "loading":
                self.loading,
        }


model_manager = ModelManager()
>>>>>>> eee99e9 (Load OmniVoice model from local Drive and improve startup)
