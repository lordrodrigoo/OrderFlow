from decimal import Decimal
from src.domain.models.order import Order, OrderStatus
from src.dto.request.order_request import OrderRequest
from src.dto.response.order_response import OrderResponse
from src.domain.repositories.order_repository import OrderRepositoryInterface
from src.exceptions.exception_handlers_order import (
    OrderNotFoundException,
    OrderAlreadyCanceledException
)


class OrderUsecase:
    def __init__(self, order_repository: OrderRepositoryInterface):
        self.order_repository = order_repository


    def create_order(self, order_request: OrderRequest, user_id: int) -> OrderResponse:
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
        return OrderResponse(**created_order.__dict__)



    def update_order(self, order_id: int, order_request: OrderRequest) -> OrderResponse:
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise OrderNotFoundException(order_id=order_id)

        order.address_id = order_request.address_id
        order.total_amount = order_request.total_amount
        order.delivery_fee = order_request.delivery_fee
        order.notes = order_request.notes
        order.scheduled_date = order_request.scheduled_date

        self.order_repository.update_order(order)
        return OrderResponse(**order.__dict__)


    def get_order_by_id(self, order_id: int) -> OrderResponse:
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
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
        orders = []

        if order_status:
            orders = self.order_repository.find_orders_by_status(order_status)
        elif user_id:
            orders = self.order_repository.find_orders_by_user(user_id)
        elif min_amount is not None and max_amount is not None:
            orders = self.order_repository.find_orders_by_total_amount(min_amount, max_amount)
        else:
            orders = self.order_repository.get_all_orders()

        # Apply pagination
        orders = orders[skip:skip + limit]
        return [OrderResponse(**order.__dict__) for order in orders]




    def cancel_order(self, order_id: int) -> OrderResponse:
        order = self.order_repository.get_order_by_id(order_id)
        if order.is_canceled:
            raise OrderAlreadyCanceledException(order_id=order_id)

        order.status = OrderStatus.CANCELED
        self.order_repository.update_order(order)
        return OrderResponse(**order.__dict__)


    def delete_order(self, order_id: int) -> bool:
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise OrderNotFoundException(order_id=order_id)

        return self.order_repository.delete_order(order_id)
