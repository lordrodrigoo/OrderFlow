from fastapi import APIRouter
from src.usecases.user_usecases import CreateUserUsecase
from src.infra.db.repositories.user_repository_interface import UserRepository
from src.infra.db.repositories.account_user_repository_interface import AccountRepository
from src.infra.db.settings.connection import DBConnectionHandler
from src.dto.request.user_request import CreateUserRequest
from src.dto.response.user_response import UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["users"])

db_handler = DBConnectionHandler()
user_repository = UserRepository(db_handler)
account_repository = AccountRepository(db_handler)
create_user_usecase = CreateUserUsecase(user_repository, account_repository)

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_request: CreateUserRequest):
    return create_user_usecase.create_user(user_request)
