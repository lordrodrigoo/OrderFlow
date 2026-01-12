from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from src.domain.models.user import Users

class UserRepositoryInterface(ABC):
    @abstractmethod
    def insert_user(
        self,
        first_name: str,
        last_name: str,
        password_hash: str,
        age: int,
        phone: str,
        email: str,
        is_active: bool,
        created_at: datetime,
        updated_at: datetime
    ) -> Users:
        pass

    @abstractmethod
    def select_user(self, first_name: str) -> List[Users]: pass


