from pydantic import BaseModel
from src.domain.models.user import UserRole


class RoleUpdateRequest(BaseModel):
    role: UserRole
