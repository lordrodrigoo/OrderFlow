# pylint: disable=duplicate-code
from datetime import datetime
from src.dto.base import BaseResponse


class AddressResponse(BaseResponse):
    id: int
    user_id: int
    street: str
    number: str
    complement: str | None
    neighborhood: str
    city: str
    state: str
    zip_code: str
    is_default: bool
    created_at: datetime
