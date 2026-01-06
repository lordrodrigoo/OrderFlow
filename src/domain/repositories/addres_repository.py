from abc import ABC, abstractmethod
from src.domain.models.address import Address


class AddressRepository(ABC):
    @abstractmethod
    def list(self) -> list[Address]:
        pass

    @abstractmethod
    def add(self, address: Address) -> Address:
        pass

    @abstractmethod
    def get_by_id(self, address_id: str) -> Address:
        pass

    @abstractmethod
    def update(self, address: Address) -> Address:
        pass

    @abstractmethod
    def delete(self, address_id: str) -> None:
        pass
