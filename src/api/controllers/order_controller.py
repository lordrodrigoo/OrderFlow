import os
import logging
from typing import List, Optional
from fastapi import APIRouter, Response, Query, status, Depends
from src.usecases.order_usecases import OrderUsecase
from src.dto.request.order_request import OrderRequest
from src.dto.response.order_response import OrderResponse
from src.api.dependencies import get_order_usecase, get_current_user


API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
ORDER_PREFIX = f"{API_V1_PREFIX}/orders"

router = APIRouter(prefix=ORDER_PREFIX, tags=["orders"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_request: OrderRequest,
    response: Response,
    current_user=Depends(get_current_user),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to create a new order."""
    logger.info("Creating order", extra={"user_id": current_user.id})
    order = order_usecase.create_order(order_request, current_user.id)
    response.headers['Location'] = f"{ORDER_PREFIX}/{order.id}"
    return order


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order_by_id(
    order_id: int,
    response: Response,
    current_user=Depends(get_current_user),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to get an order by order_id."""
    order = order_usecase.get_order_by_id(order_id, current_user.id)
    response.headers['Location'] = f"{ORDER_PREFIX}/{order.id}"
    return order


@router.get("/", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def list_orders(
    order_status: Optional[str] = Query(None, description="Filter orders by status"),
    min_amount: Optional[float] = Query(None, description="Minimum total amount"),
    max_amount: Optional[float] = Query(None, description="Maximum total amount"),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Maximum number of records to return"),
    response: Response = None,
    current_user=Depends(get_current_user),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to list orders with optional filters and pagination."""
    orders = order_usecase.list_orders(
        user_id=current_user.id,
        order_status=order_status,
        min_amount=min_amount,
        max_amount=max_amount,
        skip=skip,
        limit=limit
    )
    if response is not None:
        response.headers['Location'] = f"{ORDER_PREFIX}/"
    return orders


@router.put("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def update_order(
    order_id: int,
    order_request: OrderRequest,
    response: Response,
    current_user=Depends(get_current_user),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to update an existing order."""
    updated_order = order_usecase.update_order(order_id, order_request, current_user.id)
    response.headers['Location'] = f"{ORDER_PREFIX}/{updated_order.id}"
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    current_user=Depends(get_current_user),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to delete an order."""
    logger.info("Deleting order", extra={"order_id": order_id})
    order_usecase.delete_order(order_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{order_id}/cancel", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order(
    order_id: int,
    response: Response,
    current_user=Depends(get_current_user),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to cancel an order."""
    logger.info("Canceling order", extra={"order_id": order_id})
    canceled_order = order_usecase.cancel_order(order_id, current_user.id)
    response.headers['Location'] = f"{ORDER_PREFIX}/{canceled_order.id}"
    return canceled_order
