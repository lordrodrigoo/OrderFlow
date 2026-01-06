from abc import ABC, abstractmethod
from src.domain.models.order_item import OrderItem


class OrderItemRepository(ABC):
    @abstractmethod
    def add(self, order_item: OrderItem) -> None:
        pass

    @abstractmethod
    def get_by_id(self, order_item_id: int) -> OrderItem:
        pass

    @abstractmethod
    def list_all(self) -> list[OrderItem]:
        pass

    @abstractmethod
    def remove(self, order_item_id: int) -> None:
        pass
