from datetime import datetime
from pydantic import EmailStr
from src.dto.base import BaseResponse
from src.domain.models.user import UserRole


class UserResponse(BaseResponse):
    id: int
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    phone: str
    is_active: bool
    role: UserRole
    created_at: datetime
