from fastapi import APIRouter
from src.api.dtos.user_request import CreateUserRequest
from src.api.dtos.user_response import UserResponse
from src.usecases.user_usecases import CreateUserUsecase
from src.infra.db.repositories.user_repository_interface import UserRepository
from src.infra.db.settings.connection import DBConnectionHandler

router = APIRouter(prefix="/api/v1/users", tags=["users"])

db_handler = DBConnectionHandler()
user_repository = UserRepository(db_handler)
create_user_usecase = CreateUserUsecase(user_repository)

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_request: CreateUserRequest):
    return create_user_usecase.create_user(user_request)
