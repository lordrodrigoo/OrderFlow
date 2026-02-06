import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from src.domain.models.user import UserRole


class CreateUserRequest(BaseModel):
    # ... means required field
    # property ge means greater than or equal to
    # property le means less than or equal to
    first_name: str = Field(
        ...,
        min_length=3,
        max_length=25,
        description="first name must be between 3 and 25 characters",
    )
    last_name: str = Field(
        ...,
        min_length=3,
        max_length=25,
        description="last name must be between 3 and 25 characters",
    )
    age: int = Field(
        ...,
        ge=16,
        description="age must be at least 16 years old",
    )
    email: EmailStr = Field(
        ...,
        description="email address must be valid"
    )
    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="phone number must be between 10 and 15 characters",
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="username must be between 3 and 50 characters",
    )
    role: UserRole = Field(
        UserRole.USER,
        description="role of the user, default is USER"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="password must be at least 8 characters long"
    )


    @field_validator("first_name", "last_name")
    @classmethod
    def field_names_must_be_alpha(cls, field: str) -> str:
        if not field.isalpha():
            raise ValueError("must contain only alphabetic characters")
        return field

    @field_validator("phone")
    @classmethod
    def phone_must_be_numeric(cls, phone: str) -> str:
        if not phone.isdigit():
            raise ValueError("must contain only numeric characters")
        return phone


    @field_validator("password")
    @classmethod
    # Minimum eight characters, at least one uppercase letter, and one special character
    def validate_password(cls, password: str) -> str:
        pattern = r'^(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if not re.match(pattern, password):
            raise ValueError(
                "Password must contain at least one uppercase letter "
                "and one special character"
            )
        return password
