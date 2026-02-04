from pydantic import BaseModel, Field


class CreateAccountRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="username must be between 3 and 50 characters long"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="password must be at least 6 characters long"
    )
