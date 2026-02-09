import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, Query
from src.auth.dependencies import get_current_user
from src.usecases.user_usecases import UserUsecase
from src.infra.db.repositories.user_repository_interface import UserRepository
from src.infra.db.repositories.account_user_repository_interface import AccountRepository
from src.infra.db.settings.connection import DBConnectionHandler
from src.dto.request.user_request import CreateUserRequest
from src.dto.response.user_response import UserResponse

load_dotenv()
API_PREFIX = os.getenv("API_V1_USER")
TAG = os.getenv("TAG_USER")
router = APIRouter(prefix=API_PREFIX, tags=[TAG])

db_handler = DBConnectionHandler()
user_repository = UserRepository(db_handler)
account_repository = AccountRepository(db_handler)
user_usecase = UserUsecase(user_repository, account_repository)


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_request: CreateUserRequest, response: Response):
    """Endpoint to create a new user."""
    user = user_usecase.create_user(user_request)
    response.headers['Location'] = f"{API_PREFIX}/{user.id}"
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, response: Response):
    """Endpoint to get a user by user_id."""
    user = user_usecase.get_user_by_id(user_id)
    response.headers['Location'] = f"{API_PREFIX}/{user.id}"
    return user


@router.get("/", response_model=List[UserResponse])
def list_users(
    name: Optional[str] = Query(None, description="Filter users by name"),
    email: Optional[str] = Query(None, description="Filter users by email"),
    active: Optional[bool] = Query(None, description="Filter users by active status"),
    skip: int = 0,
    limit: int = 10,
) -> List[UserResponse]:

    """Endpoint to list users with optional filters."""
    users = user_usecase.list_users(name, email, active, skip, limit)
    return users


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_request: CreateUserRequest,
    current_user = Depends(get_current_user)
):
    """Endpoint to update an existing user."""
    updated_user = user_usecase.update_user(user_id, user_request, current_user)
    return updated_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    """Endpoint to delete a user."""
    user_usecase.delete_user(user_id)
    return Response(status_code=204)



@router.get("/me", response_model=UserResponse)
def read_users_me(current_user=Depends(get_current_user)):
    """Endpoint to get the current logged-in user."""
    return UserResponse.model_validate(current_user)
