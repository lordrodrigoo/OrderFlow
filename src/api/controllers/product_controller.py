import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import APIRouter, Response, Query, status, Depends
from src.usecases.product_usecases import ProductUsecase
from src.dto.request.product_request import ProductRequest
from src.dto.response.product_response import ProductResponse
from src.api.dependencies import get_product_usecase


load_dotenv()
API_PREFIX = os.getenv("API_V1_PRODUCT")
TAG = os.getenv("TAG_PRODUCT")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_request: ProductRequest,
    response: Response,
    product_usecase: ProductUsecase = Depends(get_product_usecase)
):
    """Endpoint to create a new product."""
    product = product_usecase.create_product(product_request)
    response.headers['Location'] = f"{API_PREFIX}/{product.id}"
    return product


@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product_by_id(
    product_id: int,
    response: Response,
    product_usecase: ProductUsecase = Depends(get_product_usecase)
):
    """Endpoint to get a product by product_id."""
    product = product_usecase.get_product_by_id(product_id)
    response.headers['Location'] = f"{API_PREFIX}/{product.id}"
    return product


@router.get("/category/{category_id}", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
def find_products_by_category(
    category_id: int,
    response: Response,
    product_usecase: ProductUsecase = Depends(get_product_usecase)
):
    """Endpoint to find products by category_id."""
    products = product_usecase.find_products_by_category(category_id)
    response.headers['Location'] = f"{API_PREFIX}/category/{category_id}"
    return products



@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
def list_products(
    name: Optional[str] = Query(None, description="Filter products by name"),
    category_id: Optional[int] = Query(None, description="Filter products by category ID"),
    available: Optional[bool] = Query(None, description="Filter products by availability"),
    min_price: Optional[float] = Query(None, description="Filter products by minimum price"),
    max_price: Optional[float] = Query(None, description="Filter products by maximum price"),
    skip: int = 0,
    limit: int = 10,
    product_usecase: ProductUsecase = Depends(get_product_usecase)
) -> List[ProductResponse]:

    """Endpoint to list products with optional filters."""
    products = product_usecase.list_products(
        name,
        category_id,
        available,
        min_price,
        max_price,
        skip,
        limit
    )
    return products



@router.get("/count/category/{category_id}", response_model=int, status_code=status.HTTP_200_OK)
def count_products_by_category(
    category_id: int,
    product_usecase: ProductUsecase = Depends(get_product_usecase)
):
    """Endpoint to count products by category_id."""
    return product_usecase.count_products_by_category(category_id)



@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(
    product_id: int,
    product_request: ProductRequest,
    response: Response,
    product_usecase: ProductUsecase = Depends(get_product_usecase)
):
    """Endpoint to update a product by product_id."""
    updated_product = product_usecase.update_product(product_id, product_request)
    response.headers['Location'] = f"{API_PREFIX}/{updated_product.id}"
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    product_usecase: ProductUsecase = Depends(get_product_usecase)):
    """Endpoint to delete a product by product_id."""
    product_usecase.delete_product(product_id)
