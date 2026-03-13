import os
from typing import List, Optional
from fastapi import APIRouter, Response, Query, status, Depends
from src.usecases.address_usecase import AddressUsecase
from src.usecases.user_usecases import UserUsecase
from src.dto.request.address_request import AddressRequest
from src.dto.response.address_response import AddressResponse
from src.api.dependencies import get_address_usecase
from src.dto.request.user_request import UserRequest
from src.dto.response.user_response import UserResponse
from src.api.dependencies import get_user_usecase, get_current_user



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


@router.post("/me/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def add_address(
    address_request: AddressRequest,
    current_user: UserResponse = Depends(get_current_user),
    address_usecase: AddressUsecase = Depends(get_address_usecase)
):
    """Endpoint to add a new address for the authenticated user."""
    address_request.user_id = current_user.id
    return address_usecase.create_address(address_request)


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


@router.get("/me/address", response_model=UserResponse, status_code=status.HTTP_200_OK)
def list_my_addresses(
    current_user: UserResponse = Depends(get_current_user),
    address_usecase: AddressUsecase = Depends(get_address_usecase)
):
    """Endpoint to list the authenticated user's addresses."""
    return address_usecase.find_addresses_by_user_id(current_user.id)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Endpoint to get the authenticated user's own information."""
    return current_user


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


@router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_me(
    user_request: UserRequest,
    current_user: UserResponse = Depends(get_current_user),
    user_usecase: UserUsecase = Depends(get_user_usecase)
):
    """Endpoint to update the authenticated user's own information."""
    updated_user = user_usecase.update_me(user_request, current_user)
    return updated_user



@router.put("/me/addresses/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address_request: AddressRequest,
    current_user: UserResponse = Depends(get_current_user),
    address_usecase: AddressUsecase = Depends(get_address_usecase)
):
    """Endpoint to update the authenticated user's address."""
    address_request.user_id = current_user.id
    return address_usecase.update_address(address_id, address_request, current_user)


@router.patch(
        "/me/addresses/{address_id}/default",
        response_model=AddressResponse,
        status_code=status.HTTP_200_OK
)
def set_default_address(
    address_id: int,
    current_user: UserResponse = Depends(get_current_user),
    address_usecase: AddressUsecase = Depends(get_address_usecase)
):
    """Endpoint to set the authenticated user's address as default."""
    return address_usecase.set_default_address(address_id, current_user.id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, user_usecase: UserUsecase = Depends(get_user_usecase)):
    """Endpoint to delete a user."""
    user_usecase.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
