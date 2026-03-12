import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator


PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
USERNAME_PATTERN = re.compile(r'^[A-Za-zÀ-ÿ0-9._]+$')


class AccountRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    username: str = Field(..., min_length=3, max_length=50, description="Username ex: 'john_doe'")
    password: str = Field(..., min_length=8, description="Password ex: 'P@ssw0rd'")


    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not PASSWORD_PATTERN.match(value):
            raise ValueError("must contain at least one uppercase, one lowercase and one special character.")
        return value

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_PATTERN.match(value):
            raise ValueError("must contain only letters, numbers, dots or underscores.")
        return value


class UpdateAccountRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)


    @field_validator("username")
    @classmethod
    def validate_username(cls, value: Optional[str]) -> Optional[str]:
        if value and not USERNAME_PATTERN.match(value):
            raise ValueError("must contain only letters, numbers, dots or underscores.")
        return value



class UpdatePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not PASSWORD_PATTERN.match(value):
            raise ValueError("must contain at least one uppercase, one lowercase and one special character.")
        return value
