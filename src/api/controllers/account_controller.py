import os
from dotenv import load_dotenv
from fastapi import APIRouter, Response, status, Depends
from src.dto.response.account_response import AccountResponse
from src.dto.request.account_request import CreateAccountRequest
from src.usecases.account_usecases import CreateAccountUsecase
from src.api.dependencies import get_account_usecase


load_dotenv()
API_PREFIX = os.getenv("API_V1_ACCOUNT")
TAG = os.getenv("TAG_ACCOUNT")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])


@router.post("/", response_model=AccountResponse,status_code=status.HTTP_201_CREATED)
def create_account(
    account_request: CreateAccountRequest,
    response: Response,
    create_account_usecase: CreateAccountUsecase = Depends(get_account_usecase)
):
    """Endpoint to create a new account for the authenticated user."""
    # account_request.user_id = current_user
    response.headers['Location'] = f"{API_PREFIX}/{account_request.id}"
    return create_account_usecase.create_account(account_request)
