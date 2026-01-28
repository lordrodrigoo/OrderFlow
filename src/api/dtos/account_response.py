from datetime import datetime
from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    username: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
