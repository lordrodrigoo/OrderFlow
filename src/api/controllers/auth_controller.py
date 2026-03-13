import os
from fastapi import APIRouter, Depends, status
from src.dto.request.refresh_token_request import RefreshTokenRequest
from src.dto.request.login_request import LoginRequest
from src.dto.response.token_response import TokenResponse
from src.usecases.auth_usecases import AuthUseCases
from src.api.dependencies import get_auth_usecase



API_PREFIX = os.getenv("API_V1_LOGIN")
TAG = os.getenv("TAG_LOGIN")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])


@router.post("/", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    login_request: LoginRequest,
    auth_usecase: AuthUseCases = Depends(get_auth_usecase)
):
    """Endpoint to authenticate a user and return a token."""
    return auth_usecase.login(login_request.username, login_request.password)


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def refresh_token(
    refresh_request: RefreshTokenRequest,
    auth_usecase: AuthUseCases = Depends(get_auth_usecase)
):
    """Endpoint to refresh an access token using a refresh token."""
    return auth_usecase.refresh_token(refresh_request.refresh_token)
