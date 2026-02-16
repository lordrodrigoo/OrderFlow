from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware


# MIDDLEWARES
def setup_middlewares(app: FastAPI):
    app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=5)
