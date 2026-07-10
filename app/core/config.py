from pathlib import Path


class Settings:
    """
    Global application settings.
    """

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME = "OmniVoice Server"

    VERSION = "2.0.0"

    HOST = "0.0.0.0"

    PORT = 8000

    DEBUG = False

    # ==========================================================
    # Project Directories
    # ==========================================================

    ROOT_DIR = Path(__file__).resolve().parents[2]

    APP_DIR = ROOT_DIR / "app"

    STORAGE_DIR = APP_DIR / "storage"

    AUDIO_DIR = STORAGE_DIR / "audio"

    TEMP_DIR = STORAGE_DIR / "temp"

    LOG_DIR = ROOT_DIR / "logs"

    # ==========================================================
    # OmniVoice
    # ==========================================================

    MODEL_NAME = "k2-fsa/OmniVoice"

    LOAD_ASR = False

    # ==========================================================
    # API
    # ==========================================================

    API_TITLE = APP_NAME

    API_VERSION = VERSION


settings = Settings()

# ==========================================================
# Create directories automatically
# ==========================================================

settings.STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

settings.AUDIO_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

settings.TEMP_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

settings.LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)