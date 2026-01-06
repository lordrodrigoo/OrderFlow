from abc import ABC, abstractmethod
from src.domain.models.order import Orders

class OrderRepository(ABC):
    @abstractmethod
    def list(self) -> list[Orders]:
        pass

    @abstractmethod
    def add(self, order: Orders) -> Orders:
        pass

    @abstractmethod
    def get_by_id(self, order_id: str) -> Orders:
        pass

    @abstractmethod
    def update(self, order: Orders) -> Orders:
        pass

    @abstractmethod
    def delete(self, order_id: str) -> None:
        pass
