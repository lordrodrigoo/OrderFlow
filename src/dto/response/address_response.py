from datetime import datetime
from pydantic import BaseModel


class AddressResponse(BaseModel):
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
    is_default: bool

    model_config = {"from_attributes": True}
