import os
from fastapi import APIRouter, Response, status, Depends
from src.api.dependencies import get_account_usecase, get_current_user
from src.dto.response.account_response import AccountResponse
from src.dto.response.user_response import UserResponse
from src.usecases.account_usecases import AccountUsecase
from src.dto.response.token_response import TokenResponse
from src.dto.request.login_request import LoginRequest
from src.dto.request.account_request import (
    AccountRequest,
    UpdateAccountRequest,
    UpdatePasswordRequest
)



API_PREFIX = os.getenv("API_V1_ACCOUNT")
TAG = os.getenv("TAG_ACCOUNT")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])



@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    login_request: LoginRequest,
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to authenticate a user and return a token."""
    return account_usecase.login(login_request)


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_request: AccountRequest,
    response: Response,
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to create a new user account."""
    account = account_usecase.create_account(account_request)
    response.headers['Location'] = f"{API_PREFIX}/{account.id}"
    return account


@router.get("/{account_id}", response_model=AccountResponse, status_code=status.HTTP_200_OK)
def get_account_by_id(
    account_id: int,
    account_usecase: AccountUsecase = Depends(get_account_usecase),
    _: UserResponse = Depends(get_current_user),
):
    """Endpoint to retrieve account details by ID."""
    return account_usecase.get_account_by_id(account_id)


@router.put("/{account_id}", response_model=AccountResponse, status_code=status.HTTP_200_OK)
def update_account(
    account_id: int,
    account_request: UpdateAccountRequest,
    current_user: UserResponse = Depends(get_current_user),
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to update account details."""
    return account_usecase.update_account(account_id, account_request, current_user.id)


@router.patch(
    "/{account_id}/password",
    response_model=AccountResponse,
    status_code=status.HTTP_200_OK
)
def update_password(
    account_id: int,
    password_request: UpdatePasswordRequest,
    current_user: UserResponse = Depends(get_current_user),
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to update account password."""
    return account_usecase.update_password(account_id, password_request, current_user.id)


@router.patch("/{account_id}/deactivate", response_model=AccountResponse, status_code=status.HTTP_200_OK)
def deactivate_account(
    account_id: int,
    current_user: UserResponse = Depends(get_current_user),
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to deactivate an account."""
    return account_usecase.deactivate_account(account_id, current_user.id)


@router.patch("/{account_id}/suspended", response_model=AccountResponse, status_code=status.HTTP_200_OK)
def suspend_account(
    account_id: int,
    current_user: UserResponse = Depends(get_current_user),
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to suspend an account."""
    return account_usecase.suspend_account(account_id, current_user.id)

@router.patch("/{account_id}/activate", response_model=AccountResponse, status_code=status.HTTP_200_OK)
def activate_account(
    account_id: int,
    current_user: UserResponse = Depends(get_current_user),
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to activate an account."""
    return account_usecase.activate_account(account_id, current_user.id)


@router.patch("/{account_id}/inactive", response_model=AccountResponse, status_code=status.HTTP_200_OK)
def inactivate_account(
    account_id: int,
    current_user: UserResponse = Depends(get_current_user),
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to inactivate an account."""
    return account_usecase.inactivate_account(account_id, current_user.id)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: int,
    current_user: UserResponse = Depends(get_current_user),
    account_usecase: AccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to delete an account."""
    account_usecase.delete_account(account_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
