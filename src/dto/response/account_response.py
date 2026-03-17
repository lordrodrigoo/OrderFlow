from datetime import datetime
from src.dto.base import BaseResponse


class AccountResponse(BaseResponse):
    id: int
    username: str
    status: str
    created_at: datetime
