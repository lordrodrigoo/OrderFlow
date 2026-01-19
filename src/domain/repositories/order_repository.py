from decimal import Decimal
from abc import ABC, abstractmethod
from src.domain.models.order import Order


class OrderRepositoryInterface(ABC):
    """This interface defines the contract for order repository."""

    @abstractmethod
    def create_order(self, order: Order) -> Order: pass

    @abstractmethod
    def update_order(self, order: Order) -> Order: pass

    @abstractmethod
    def cancel_order(self, order_id: int) -> bool: pass

    @abstractmethod
    def find_orders_by_user(self, user_id: int) -> list[Order]: pass

    @abstractmethod
    def find_orders_by_total_amount(self, min_amount: Decimal, max_amount: Decimal) -> list[Order]: pass

    @abstractmethod
    def find_orders_by_status(self, status: str) -> list[Order]: pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Order | None: pass

    @abstractmethod
    def get_all_orders(self) -> list[Order]: pass

    @abstractmethod
    def delete_order(self, order_id: int) -> bool: pass
