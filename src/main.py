#pylint: disable=unused-import
from dotenv import load_dotenv
from fastapi import FastAPI
from src.middlewares.middlewares import setup_middlewares
from src.exceptions.handlers import register_exception_handlers
from src.api.controllers.routers import include_routers
from src.config.settings import Settings


load_dotenv()
app = FastAPI(title=Settings.API_TITLE, version=Settings.API_VERSION)


# MIDDLEWARE
setup_middlewares(app)


# EXCEPTION HANDLERS
register_exception_handlers(app)


# ROUTERS
include_routers(app)
