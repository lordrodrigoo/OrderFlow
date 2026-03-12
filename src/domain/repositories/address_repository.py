from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.address import Address


class AddressRepositoryInterface(ABC):
    """This interface defines the contract for address repository."""

    @abstractmethod
    def create_address(self, address: Address) -> Address: pass

    @abstractmethod
    def update_address(self, address: Address) -> Address: pass

    @abstractmethod
    def find_all_addresses(self) -> List[Address]: pass

    @abstractmethod
    def find_address_by_id(self, address_id: int) -> Optional[Address]: pass

    @abstractmethod
    def find_addresses_by_user_id(self, user_id: int) -> List[Address]: pass

    @abstractmethod
    def find_addresses_by_user_street_number(
        self,
        user_id: int,
        street: str,
        number: str
    )-> List[Address]: pass

    @abstractmethod
    def delete_address(self, address_id: int) -> bool: pass

    @abstractmethod
    def set_default_address(self, address_id: int, user_id: int) -> Optional[Address]: pass
