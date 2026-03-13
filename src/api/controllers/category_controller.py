import os
from typing import List
from fastapi import APIRouter, Response, status, Depends
from src.usecases.category_usecases import CategoryUsecase
from src.dto.request.category_request import CategoryRequest
from src.dto.response.category_response import CategoryResponse
from src.api.dependencies import get_category_usecase



API_PREFIX = os.getenv("API_V1_CATEGORY")
TAG = os.getenv("TAG_CATEGORY")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_request: CategoryRequest,
    response: Response,
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Endpoint to create a new category."""
    category = category_usecase.create_category(category_request)
    response.headers['Location'] = f"{API_PREFIX}/{category.id}"
    return category


@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category_by_id(
    category_id: int,
    response: Response,
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Endpoint to get a category by category_id."""
    category = category_usecase.get_category_by_id(category_id)
    response.headers['Location'] = f"{API_PREFIX}/{category.id}"
    return category


@router.get("/", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def list_categories(
    response: Response,
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Endpoint to list all categories."""
    categories = category_usecase.list_categories()
    response.headers['Location'] = f"{API_PREFIX}/"
    return categories


@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(
    category_id: int,
    category_request: CategoryRequest,
    response: Response,
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Endpoint to update a category by category_id."""
    category = category_usecase.update_category(category_id, category_request)
    response.headers['Location'] = f"{API_PREFIX}/{category.id}"
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Endpoint to delete a category by category_id."""
    category_usecase.delete_category(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
