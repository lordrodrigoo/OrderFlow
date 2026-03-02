from abc import ABC, abstractmethod
from src.domain.models.order_item import OrderItem


class OrderItemRepositoryInterface(ABC):
    """This interface defines the contract for order item repository."""

    @abstractmethod
    def create_order_item(self, order_item: OrderItem) -> OrderItem: pass

    @abstractmethod
    def update_order_item(self, order_item: OrderItem) -> OrderItem: pass

    @abstractmethod
    def get_order_item_by_id(self, order_item_id: int) -> OrderItem | None: pass

    @abstractmethod
    def get_all_order_items(self) -> list[OrderItem]: pass

    @abstractmethod
    def delete_order_item(self, order_item_id: int) -> bool: pass

    @abstractmethod
    def exists(self, order_id: int, product_id: int) -> bool: pass

    @abstractmethod
    def get_order_items_by_order_id(self, order_id: int) -> list[OrderItem]: pass
