import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.monotonic()

        correlation_id = getattr(request.state, "correlation_id", "-")

        logger.info(
            "Incoming request",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
            },
        )

        response = await call_next(request)

        duration_ms = round((time.monotonic() - start_time) * 1000, 2)

        logger.info(
            "Request completed",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

        return response
