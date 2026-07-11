from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.errors import OmniVoiceError
from app.core.logger import logger
from app.models import ApiResponse


async def global_exception_handler(
    request: Request,
    exc: OmniVoiceError,
):

    logger.exception(exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            success=False,
            message=exc.message,
            data=None,
        ).model_dump(),
    )