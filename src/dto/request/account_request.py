import re
from pydantic import BaseModel, Field, field_validator


class CreateAccountRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="username must be between 3 and 50 characters long"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="password must be at least 8 characters long"
    )


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
