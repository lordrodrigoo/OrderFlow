import os
import logging
from typing import List, Optional
from fastapi import APIRouter, Response, Query, status, Depends
from src.usecases.order_usecases import OrderUsecase
from src.usecases.user_usecases import UserUsecase
from src.usecases.product_usecases import ProductUsecase
from src.dto.request.order_status_request import OrderStatusUpdateRequest
from src.dto.response.order_response import OrderResponse
from src.dto.response.dashboard_response import DashboardResponse
from src.dto.response.user_response import UserResponse
from src.api.dependencies import get_order_usecase, get_user_usecase, get_product_usecase, get_current_admin

API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
ADMIN_PREFIX = f"{API_V1_PREFIX}/admin"


router = APIRouter(prefix=ADMIN_PREFIX, tags=["admin"])
logger = logging.getLogger(__name__)


@router.patch("/orders/{order_id}/status", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def update_order_status(
    order_id: int,
    status_request: OrderStatusUpdateRequest,
    response: Response,
    current_admin: UserResponse = Depends(get_current_admin),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Admin endpoint to update the status of any order."""
    logger.info("Admin updating order status", extra={"order_id": order_id, "admin_id": current_admin.id})
    updated_order = order_usecase.admin_update_order_status(order_id, status_request.status)
    response.headers["Location"] = f"{ADMIN_PREFIX}/orders/{updated_order.id}"
    return updated_order


@router.get("/orders", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def list_all_orders(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    order_status: Optional[str] = Query(None, description="Filter by order status"),
    min_amount: Optional[float] = Query(None, description="Minimum total amount"),
    max_amount: Optional[float] = Query(None, description="Maximum total amount"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    current_admin: UserResponse = Depends(get_current_admin),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Admin endpoint to list all orders with optional filters."""
    logger.info("Admin listing all orders", extra={"admin_id": current_admin.id})
    return order_usecase.admin_get_all_orders(
        order_status=order_status,
        user_id=user_id,
        min_amount=min_amount,
        max_amount=max_amount,
        skip=skip,
        limit=limit
    )


@router.get("/dashboard", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
def get_dashboard(
    current_admin: UserResponse = Depends(get_current_admin),
    order_usecase: OrderUsecase = Depends(get_order_usecase),
    user_usecase: UserUsecase = Depends(get_user_usecase),
    product_usecase: ProductUsecase = Depends(get_product_usecase)
):
    """Admin dashboard with overall system statistics."""
    logger.info("Admin accessing dashboard", extra={"admin_id": current_admin.id})
    total_users = user_usecase.get_total_users()
    total_products = product_usecase.get_total_products()
    return order_usecase.get_dashboard_stats(total_users, total_products)
