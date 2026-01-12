from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from src.domain.models.address import Address

class AddressRepositoryInterface(ABC):
    @abstractmethod
    def insert_address(
        self,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
        created_at: datetime,
        updated_at: datetime
    ) -> Address:
        pass

    @abstractmethod
    def select_address(self, street: str) -> List[Address]: pass
