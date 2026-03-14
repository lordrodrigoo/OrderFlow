import os
from typing import List, Optional
from fastapi import APIRouter, Response, Query, status, Depends
from src.usecases.order_usecases import OrderUsecase
from src.dto.request.order_request import OrderRequest
from src.dto.response.order_response import OrderResponse
from src.api.dependencies import get_order_usecase, get_current_user


API_PREFIX = os.getenv("API_V1_ORDER")
TAG = os.getenv("TAG_ORDER")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_request: OrderRequest,
    response: Response,
    current_user=Depends(get_current_user),
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to create a new order."""
    order = order_usecase.create_order(order_request, current_user.id)
    response.headers['Location'] = f"{API_PREFIX}/{order.id}"
    return order


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def get_order_by_id(
    order_id: int,
    response: Response,
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to get an order by order_id."""
    order = order_usecase.get_order_by_id(order_id)
    response.headers['Location'] = f"{API_PREFIX}/{order.id}"
    return order


@router.get("/", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def list_orders(
    user_id: Optional[int] = Query(None, description="Filter orders by user ID"),
    order_status: Optional[str] = Query(None, description="Filter orders by status"),
    min_amount: Optional[float] = Query(None, description="Minimum total amount"),
    max_amount: Optional[float] = Query(None, description="Maximum total amount"),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Maximum number of records to return"),
    response: Response = None,
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to list orders with optional filters and pagination."""
    orders = order_usecase.list_orders(
        user_id=user_id,
        order_status=order_status,
        min_amount=min_amount,
        max_amount=max_amount,
        skip=skip,
        limit=limit
    )
    if response is not None:
        response.headers['Location'] = f"{API_PREFIX}/"
    return orders


@router.put("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def update_order(
    order_id: int,
    order_request: OrderRequest,
    response: Response,
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to update an existing order."""
    updated_order = order_usecase.update_order(order_id, order_request)
    response.headers['Location'] = f"{API_PREFIX}/{updated_order.id}"
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to delete an order."""
    order_usecase.delete_order(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{order_id}/cancel", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def cancel_order(
    order_id: int,
    response: Response,
    order_usecase: OrderUsecase = Depends(get_order_usecase)
):
    """Endpoint to cancel an order."""
    canceled_order = order_usecase.cancel_order(order_id)
    response.headers['Location'] = f"{API_PREFIX}/{canceled_order.id}"
    return canceled_order
