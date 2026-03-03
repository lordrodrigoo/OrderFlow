from typing import Optional
from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
