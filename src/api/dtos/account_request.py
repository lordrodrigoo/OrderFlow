from pydantic import BaseModel, Field


class CreateAccountRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Your username")
    password: str = Field(..., min_length=6, description="Your password")
