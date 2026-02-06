from datetime import datetime
from pydantic import BaseModel, EmailStr
from src.domain.models.user import UserRole


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    phone: str
    is_active: bool
    role: UserRole
    created_at: datetime

    model_config = {"from_attributes": True}
