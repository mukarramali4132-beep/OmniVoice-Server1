from loguru import logger
import sys

from app.core.config import settings


logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
)

logger.add(
    settings.LOG_DIR / "server.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    enqueue=True,
)

__all__ = [
    "logger",
]