import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import APIRouter, Response, Query, status, Depends
from src.usecases.order_item_usecases import OrderItemUsecase
from src.dto.request.order_item_request import OrderItemRequest
from src.dto.response.order_item_response import OrderItemResponse
from src.api.dependencies import get_order_item_usecase


load_dotenv()
API_PREFIX = os.getenv("API_V1_ORDER_ITEM")
TAG = os.getenv("TAG_ORDER_ITEM")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])

@router.post("/", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def create_order_item(
    order_item_request: OrderItemRequest,
    response: Response,
    order_item_usecase: OrderItemUsecase = Depends(get_order_item_usecase)
):
    """Endpoint to create a new order item."""
    order_item = order_item_usecase.create_order_item(order_item_request)
    response.headers['Location'] = f"{API_PREFIX}/{order_item.id}"
    return order_item


@router.put("/{order_item_id}", response_model=OrderItemResponse, status_code=status.HTTP_200_OK)
def update_order_item(
    order_item_id: int,
    order_item_request: OrderItemRequest,
    response: Response,
    order_item_usecase: OrderItemUsecase = Depends(get_order_item_usecase)
):
    """Endpoint to update an existing order item."""
    updated_order_item = order_item_usecase.update_order_item(order_item_id, order_item_request)
    response.headers['Location'] = f"{API_PREFIX}/{updated_order_item.id}"
    return updated_order_item


@router.delete("/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(
    order_item_id: int,
    order_item_usecase: OrderItemUsecase = Depends(get_order_item_usecase)
):
    """Endpoint to delete an order item."""
    order_item_usecase.delete_order_item(order_item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{order_item_id}", response_model=OrderItemResponse, status_code=status.HTTP_200_OK)
def get_order_item_by_id(
    order_item_id: int,
    response: Response,
    order_item_usecase: OrderItemUsecase = Depends(get_order_item_usecase)
):
    """Endpoint to get an order item by order_item_id."""
    order_item = order_item_usecase.get_order_item_by_id(order_item_id)
    response.headers['Location'] = f"{API_PREFIX}/{order_item.id}"
    return order_item


@router.get("/", response_model=List[OrderItemResponse], status_code=status.HTTP_200_OK)
def list_order_items(
    order_id: Optional[int] = Query(None, description="Filter order items by order ID"),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(10, description="Maximum number of records to return"),
    response: Response = None,
    order_item_usecase: OrderItemUsecase = Depends(get_order_item_usecase)
):
    """Endpoint to list order items with optional filters and pagination."""
    order_items = order_item_usecase.list_order_items(order_id=order_id, skip=skip, limit=limit)
    if response is not None:
        response.headers['Location'] = f"{API_PREFIX}/"
    return order_items
