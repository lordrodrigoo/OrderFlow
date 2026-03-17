from typing import Optional
from src.dto.base import BaseResponse


class CategoryResponse(BaseResponse):
    id: int
    name: str
    description: Optional[str] = None
