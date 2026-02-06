import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, status
from src.auth.dependencies import get_current_user
from src.infra.db.repositories.account_user_repository_interface import AccountRepository
from src.infra.db.settings.connection import DBConnectionHandler
from src.dto.response.account_response import AccountResponse
from src.dto.request.account_request import CreateAccountRequest
from src.usecases.account_usecases import CreateAccountUsecase


load_dotenv()
API_PREFIX = os.getenv("API_V1_ACCOUNT")
TAG = os.getenv("TAG_ACCOUNT")

router = APIRouter(prefix=API_PREFIX, tags=[TAG])

db_handler = DBConnectionHandler()
account_repository = AccountRepository(db_handler)
create_account_usecase = CreateAccountUsecase(account_repository)


@router.post("/", response_model=AccountResponse,status_code=status.HTTP_201_CREATED)
def create_account(
    account_request: CreateAccountRequest,
    response: Response,
    current_user: str = Depends(get_current_user)
):
    """Endpoint to create a new account for the authenticated user."""
    account_request.user_id = current_user
    response.headers['Location'] = f"{API_PREFIX}/{account_request.id}"

    return create_account_usecase.create_account(account_request)
