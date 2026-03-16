from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from src.middlewares.logging_middleware import LoggingMiddleware
from src.middlewares.correlation_middleware import CorrelationIdMiddleware


# MIDDLEWARES
def setup_middlewares(app: FastAPI):
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=5)
