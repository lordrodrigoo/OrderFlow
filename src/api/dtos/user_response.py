from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    phone: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
