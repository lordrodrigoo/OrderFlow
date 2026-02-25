import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import APIRouter, Response, Query, status, Depends
from src.usecases.user_usecases import UserUsecase
from src.dto.request.user_request import UserRequest
from src.dto.response.user_response import UserResponse
from src.api.dependencies import get_user_usecase

load_dotenv()
API_PREFIX = os.getenv("API_V1_USER")
TAG = os.getenv("TAG_USER")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])



@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_request: UserRequest,
    response: Response,
    user_usecase: UserUsecase = Depends(get_user_usecase)
):
    """Endpoint to create a new user."""
    user = user_usecase.create_user(user_request)
    response.headers['Location'] = f"{API_PREFIX}/{user.id}"
    return user


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(
    user_id: int,
    response: Response,
    user_usecase: UserUsecase = Depends(get_user_usecase)
):
    """Endpoint to get a user by user_id."""
    user = user_usecase.get_user_by_id(user_id)
    response.headers['Location'] = f"{API_PREFIX}/{user.id}"
    return user


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(
    name: Optional[str] = Query(None, description="Filter users by name"),
    email: Optional[str] = Query(None, description="Filter users by email"),
    active: Optional[bool] = Query(None, description="Filter users by active status"),
    skip: int = 0,
    limit: int = 10,
    user_usecase: UserUsecase = Depends(get_user_usecase)
) -> List[UserResponse]:

    """Endpoint to list users with optional filters."""
    users = user_usecase.list_users(name, email, active, skip, limit)
    return users


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    user_request: UserRequest,
    current_user: None = None,
    user_usecase: UserUsecase = Depends(get_user_usecase)
):
    """Endpoint to update an existing user."""
    updated_user = user_usecase.update_user(user_id, user_request, current_user)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, user_usecase: UserUsecase = Depends(get_user_usecase)):
    """Endpoint to delete a user."""
    user_usecase.delete_user(user_id)
