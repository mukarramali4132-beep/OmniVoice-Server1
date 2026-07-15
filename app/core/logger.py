import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings


class Logger:

    def __init__(self):

        self._configure()

    def _configure(self):

        logger.remove()

        # Console Logger
        logger.add(
            sys.stdout,
            colorize=True,
            level="INFO",
            enqueue=True,
            backtrace=False,
            diagnose=False,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>",
        )

        # Local Log Directory
        log_dir = Path(settings.LOG_DIR)

        log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Server Log
        logger.add(
            log_dir / "server.log",
            level="INFO",
            enqueue=True,
            encoding="utf-8",
            rotation="10 MB",
            retention=10,
            compression="zip",
            backtrace=False,
            diagnose=False,
        )

        # Error Log
        logger.add(
            log_dir / "error.log",
            level="ERROR",
            enqueue=True,
            encoding="utf-8",
            rotation="10 MB",
            retention=20,
            compression="zip",
            backtrace=True,
            diagnose=True,
        )


Logger()
