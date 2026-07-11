from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.errors import OmniVoiceError
from app.core.exceptions import global_exception_handler
from app.core.logger import logger
from app.engine import OmniVoiceEngine

# ---------------------------------------------------------
# Engine
# ---------------------------------------------------------

engine = OmniVoiceEngine()


# ---------------------------------------------------------
# Startup / Shutdown
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 60)
    logger.info(f"{settings.APP_NAME} v{settings.VERSION}")
    logger.info("Starting server...")

    engine.initialize()

    logger.success("Server initialization completed.")

    yield

    logger.info("Stopping server...")
    logger.info("=" * 60)


# ---------------------------------------------------------
# FastAPI
# ---------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Production AI Voice Cloning Server",
    lifespan=lifespan,
)

# Handle only our business exceptions
app.add_exception_handler(
    OmniVoiceError,
    global_exception_handler,
)

# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

app.include_router(router)