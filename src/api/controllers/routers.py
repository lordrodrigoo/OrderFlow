from fastapi import FastAPI
from src.api.controllers.user_controller import router as user_router
from src.api.controllers.address_controller import router as address_router
from src.api.controllers.health import router as health_router
from src.api.controllers.product_controller import router as product_router
from src.api.controllers.category_controller import router as category_router
from src.api.controllers.order_controller import router as order_router
from src.api.controllers.order_item_controller import router as order_item_router
from src.api.controllers.review_controller import router as review_router
from src.api.controllers.account_controller import router as account_router
from src.api.controllers.auth_controller import router as login_router

def include_routers(app: FastAPI):
    app.include_router(user_router)
    app.include_router(address_router)
    app.include_router(product_router)
    app.include_router(health_router)
    app.include_router(category_router)
    app.include_router(order_router)
    app.include_router(order_item_router)
    app.include_router(review_router)
    app.include_router(account_router)
    app.include_router(login_router)
