#pylint: disable=unused-import
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from src.middlewares.middlewares import setup_middlewares
from src.exceptions.handlers import register_exception_handlers
from src.api.controllers.routers import include_routers
from src.config.settings import Settings
from src.config.logger import setup_logging
from src.config.owner import seed_owner


load_dotenv()
setup_logging()

_env = os.getenv("ENV", "production")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    seed_owner()
    yield


app = FastAPI(
    title=Settings.API_TITLE,
    version=Settings.API_VERSION,
    docs_url="/docs" if _env != "production" else None,
    redoc_url="/redoc" if _env != "production" else None,
    openapi_url="/openapi.json" if _env != "production" else None,
    lifespan=lifespan,
)


# MIDDLEWARE
setup_middlewares(app)


# EXCEPTION HANDLERS
register_exception_handlers(app)


# ROUTERS
include_routers(app)
