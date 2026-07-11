from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logger import logger
from app.models import ApiResponse


async def global_exception_handler(
    request: Request,
    exc: Exception,
):

    logger.exception(exc)

    response = ApiResponse(
        success=False,
        message=str(exc),
        data=None,
    )

    return JSONResponse(
        status_code=500,
        content=response.model_dump(),
    )