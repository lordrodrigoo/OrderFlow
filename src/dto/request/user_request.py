import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from src.domain.models.user import UserRole

USERNAME_PATTERN = re.compile(r'^[A-Za-zÀ-ÿ0-9._]+$')
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
LETTERS_ONLY = re.compile(r'^[A-Za-zÀ-ÿ\s]+$')

class UserRequest(BaseModel):
    # ... means required field
    # property ge means greater than or equal to
    # property le means less than or equal to
    first_name: str = Field(
        ...,
        min_length=3,
        max_length=25,
        description="First name ex: 'John'",
    )
    last_name: str = Field(
        ...,
        min_length=3,
        max_length=25,
        description="Last name ex: 'Doe'",
    )
    age: int = Field(
        ...,
        ge=16,
        description="Age greater than or equal to 16 years old",
    )
    email: EmailStr = Field(
        ...,
        description="Email address must be valid ex: 'example@example.com'"
    )
    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Phone number ex: '11987654321'",
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username ex: 'john_doe'",
    )
    role: UserRole = Field(
        UserRole.USER,
        description="Role of the user, default is USER"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password ex: 'P@ssw0rd' Minimum eight characters, at least one uppercase letter, and one special character"
    )


    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not LETTERS_ONLY.match(value):
            raise ValueError("must contain only letters.")
        return value


    @field_validator('age')
    @classmethod
    def validate_age(cls, value: int) -> int:
        if value > 120:
            raise ValueError("age must be less than or equal to 120 years old.")
        return value


    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("phone must contain only numeric characters.")
        return value


    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not PASSWORD_PATTERN.match(value):
            raise ValueError(
                "password must contain at least one uppercase, one lowercase and one special character.")
        return value


    @field_validator('username')
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_PATTERN.match(value):
            raise ValueError("username must contain only letters, numbers, dots or underscores.")
        return value
