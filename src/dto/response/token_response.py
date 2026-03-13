from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: str
    user_id: int
    exp: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None
