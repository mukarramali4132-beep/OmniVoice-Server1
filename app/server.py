from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logger import logger
from app.engine import OmniVoiceEngine


# ---------------------------------------------------------
# Initialize Engine
# ---------------------------------------------------------

engine = OmniVoiceEngine()


# ---------------------------------------------------------
# Application Lifecycle
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when the application starts and stops.
    """

    logger.info("=" * 60)
    logger.info(f"{settings.APP_NAME} v{settings.VERSION}")
    logger.info("Starting server...")

    try:
        engine.initialize()
        logger.success("Server initialization completed.")

    except Exception as e:
        logger.exception("Failed to initialize server.")
        raise e

    yield

    logger.info("Stopping server...")
    logger.info("=" * 60)


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Production AI Voice Cloning Server",
    lifespan=lifespan,
)

# ---------------------------------------------------------
# Register Routes
# ---------------------------------------------------------

app.include_router(router)