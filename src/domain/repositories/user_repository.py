from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.user import Users

class UserRepositoryInterface(ABC):
    """This interface defines the contract for user repository."""

    @abstractmethod
    def create_user(self, user: Users) -> Users: pass

    @abstractmethod
    def update_user(self, user: Users) -> Users: pass

    @abstractmethod
    def find_all_users(self) -> List[Users]: pass

    @abstractmethod
    def find_user_by_id(self, user_id: int) -> Optional[Users]: pass

    @abstractmethod
    def find_by_name(self, name: str) -> List[Users]: pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Users]: pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool: pass
