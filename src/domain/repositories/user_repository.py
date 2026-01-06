from abc import ABC, abstractmethod
from src.domain.models.user import Users


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: Users) -> Users:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Users:
        pass

    @abstractmethod
    def update_user(self, user: Users) -> Users:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def list_users(self) -> list[Users]:
        pass
