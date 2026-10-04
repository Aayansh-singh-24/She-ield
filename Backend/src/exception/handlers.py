
import logging
import sentry_sdk

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.exception.base import AppException
from src.exception.response import error_response

logger = logging.getLogger(__name__)


# Server-Side error Handler -> This type of Exception monitor through sentry
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    # Report unexpected server-side application errors
    if exc.status_code >= 500:
        sentry_sdk.capture_exception(exc)

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=exc.message,error_code=exc.error_code,)
    )



async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=str(exc.detail),
            error_code=f"HTTP_{exc.status_code}",
        ),
        headers=exc.headers,
    )


# Invalid Validation error handler
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content=error_response(
            message="Request validation failed",
            error_code="VALIDATION_ERROR",
            details=[
                {
                    "field": ".".join(str(part) for part in error["loc"]),
                    "message": error["msg"],
                }
                for error in exc.errors()
            ],
        ),
    )

# Interval server error handler -> These type of exception are monitor through sentry
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled exception on %s %s",
        request.method,
        request.url.path,
    )

    sentry_sdk.capture_exception(exc)

    return JSONResponse(
        status_code=500,
        content=error_response(
            message="An unexpected error occurred",
            error_code="INTERNAL_SERVER_ERROR",
        ),
    )