import logging
from decimal import Decimal
from src.domain.models.order import Order, OrderStatus
from src.dto.request.order_request import OrderRequest
from src.dto.response.order_response import OrderResponse
from src.dto.response.dashboard_response import DashboardResponse
from src.domain.repositories.order_repository import OrderRepositoryInterface
from src.domain.repositories.address_repository import AddressRepositoryInterface
from src.exceptions.exception_handlers_order import (
    OrderNotFoundException,
    OrderAlreadyCanceledException,
    OrderAddressNotFoundException
)

logger = logging.getLogger(__name__)


class OrderUsecase:
    def __init__(self, order_repository: OrderRepositoryInterface, address_repository: AddressRepositoryInterface):
        self.order_repository = order_repository
        self.address_repository = address_repository


    def create_order(self, order_request: OrderRequest, user_id: int) -> OrderResponse:
        if not self.address_repository.find_address_by_id(order_request.address_id):
            logger.warning("Address not found for order", extra={"address_id": order_request.address_id})
            raise OrderAddressNotFoundException(address_id=order_request.address_id)
        order_entity = Order(
            user_id=user_id,
            address_id=order_request.address_id,
            total_amount=order_request.total_amount,
            delivery_fee=order_request.delivery_fee,
            notes=order_request.notes,
            scheduled_date=order_request.scheduled_date,
            status=OrderStatus.PENDING
        )
        created_order = self.order_repository.create_order(order_entity)
        logger.info("Order created", extra={"order_id": created_order.id, "user_id": user_id})
        return OrderResponse(**created_order.__dict__)



    def update_order(self, order_id: int, order_request: OrderRequest, current_user_id: int) -> OrderResponse:
        order = self.order_repository.get_order_by_id(order_id)
        if not order or order.user_id != current_user_id:
            logger.warning("Order not found", extra={"order_id": order_id})
            raise OrderNotFoundException(order_id=order_id)

        order.address_id = order_request.address_id
        order.total_amount = order_request.total_amount
        order.delivery_fee = order_request.delivery_fee
        order.notes = order_request.notes
        order.scheduled_date = order_request.scheduled_date

        self.order_repository.update_order(order)
        return OrderResponse(**order.__dict__)


    def get_order_by_id(self, order_id: int, current_user_id: int) -> OrderResponse:
        order = self.order_repository.get_order_by_id(order_id)
        if not order or order.user_id != current_user_id:
            logger.warning("Order not found", extra={"order_id": order_id})
            raise OrderNotFoundException(order_id=order_id)
        return OrderResponse(**order.__dict__)


    def list_orders(
            self,
            user_id: int = None,
            order_status: OrderStatus = None,
            min_amount: Decimal = None,
            max_amount: Decimal = None,
            skip: int = 0,
            limit: int = 10
    ) -> list[OrderResponse]:
        if user_id:
            orders = self.order_repository.find_orders_by_user(user_id)
        else:
            orders = self.order_repository.get_all_orders()

        if order_status:
            orders = [o for o in orders if o.status == order_status
                      or (hasattr(o.status, "value") and o.status.value == order_status)]

        if min_amount is not None and max_amount is not None:
            orders = [o for o in orders if min_amount <= Decimal(str(o.total_amount)) <= max_amount]

        orders = orders[skip:skip + limit]
        return [OrderResponse(**order.__dict__) for order in orders]




    def cancel_order(self, order_id: int, current_user_id: int) -> OrderResponse:
        order = self.order_repository.get_order_by_id(order_id)
        if not order or order.user_id != current_user_id:
            logger.warning("Order not found", extra={"order_id": order_id})
            raise OrderNotFoundException(order_id=order_id)
        if order.is_canceled:
            logger.warning("Order already canceled", extra={"order_id": order_id})
            raise OrderAlreadyCanceledException(order_id=order_id)

        order.status = OrderStatus.CANCELED
        self.order_repository.update_order(order)
        logger.info("Order canceled", extra={"order_id": order_id})
        return OrderResponse(**order.__dict__)


    def delete_order(self, order_id: int, current_user_id: int) -> bool:
        order = self.order_repository.get_order_by_id(order_id)
        if not order or order.user_id != current_user_id:
            logger.warning("Order not found for deletion", extra={"order_id": order_id})
            raise OrderNotFoundException(order_id=order_id)
        logger.info("Order deleted", extra={"order_id": order_id})
        return self.order_repository.delete_order(order_id)


    def admin_update_order_status(self, order_id: int, new_status: str) -> OrderResponse:
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            logger.warning("Order not found for status update", extra={"order_id": order_id})
            raise OrderNotFoundException(order_id=order_id)
        order.status = new_status
        self.order_repository.update_order(order)
        logger.info("Order status updated by admin", extra={"order_id": order_id, "status": new_status})
        return OrderResponse(**order.__dict__)


    def admin_get_all_orders(
            self,
            order_status: str = None,
            user_id: int = None,
            min_amount: float = None,
            max_amount: float = None,
            skip: int = 0,
            limit: int = 10
    ) -> list[OrderResponse]:
        if order_status:
            orders = self.order_repository.find_orders_by_status(order_status)
        elif user_id:
            orders = self.order_repository.find_orders_by_user(user_id)
        elif min_amount is not None and max_amount is not None:
            orders = self.order_repository.find_orders_by_total_amount(min_amount, max_amount)
        else:
            orders = self.order_repository.get_all_orders()
        orders = orders[skip:skip + limit]
        return [OrderResponse(**order.__dict__) for order in orders]


    def get_dashboard_stats(self, total_users: int, total_products: int) -> DashboardResponse:
        all_orders = self.order_repository.get_all_orders()

        total_revenue = sum(
            float(order.total_amount)
            for order in all_orders
            if order.status != OrderStatus.CANCELED
        )

        orders_by_status: dict[str, int] = {}
        for order in all_orders:
            status_value = order.status.value if isinstance(order.status, OrderStatus) else order.status
            orders_by_status[status_value] = orders_by_status.get(status_value, 0) + 1

        return DashboardResponse(
            total_orders=len(all_orders),
            total_users=total_users,
            total_products=total_products,
            total_revenue=round(total_revenue, 2),
            orders_by_status=orders_by_status
        )
