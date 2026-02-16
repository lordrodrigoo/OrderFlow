from fastapi import FastAPI
from src.api.controllers.user_controller import router as user_router
from src.api.controllers.address_controller import router as address_router
from src.api.controllers.health import router as health_router


def include_routers(app: FastAPI):
    app.include_router(user_router)
    app.include_router(address_router)
    app.include_router(health_router)
