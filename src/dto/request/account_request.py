import re
from pydantic import BaseModel, Field, field_validator


PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
USERNAME_PATTERN = re.compile(r'^[A-Za-zÀ-ÿ0-9._]+$')


class CreateAccountRequest(BaseModel):
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
