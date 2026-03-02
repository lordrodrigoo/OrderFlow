from src.domain.models.order_item import OrderItem
from src.dto.request.order_item_request import OrderItemRequest
from src.dto.response.order_item_response import OrderItemResponse
from src.domain.repositories.order_item_repository import OrderItemRepositoryInterface
from src.domain.repositories.order_repository import OrderRepositoryInterface
from src.domain.repositories.product_repository import ProductRepositoryInterface
from src.domain.models.order import OrderStatus
from src.exceptions.exception_handlers_order_item import (
    OrderItemNotFoundException,
    InvalidOrderItemException,
    DuplicateOrderItemException
)
from src.exceptions.exception_handlers_order import OrderNotFoundException
from src.exceptions.exception_handlers_product import ProductNotFoundException


class OrderItemUsecase:
    def __init__(
        self,
        order_item_repository: OrderItemRepositoryInterface,
        product_repository: ProductRepositoryInterface,
        order_repository: OrderRepositoryInterface
    ):
        self.order_item_repository = order_item_repository
        self.product_repository = product_repository
        self.order_repository = order_repository


    def create_order_item(self, order_item_request: OrderItemRequest) -> OrderItemResponse:
        order_id = order_item_request.order_id
        product_id = order_item_request.product_id

        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise OrderNotFoundException(order_id=order_id)

        product = self.product_repository.find_product_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)

        if order.status in (OrderStatus.DELIVERED, OrderStatus.CANCELED):
            raise InvalidOrderItemException(order_id=order_id, status=order.status.value)

        if self.order_item_repository.exists(order_id, product_id):
            raise DuplicateOrderItemException(order_id=order_id, product_id=product_id)

        order_item = OrderItem.create_order_item(
            order_id=order_id,
            product_id=product_id,
            quantity=order_item_request.quantity,
            unit_price=order_item_request.unit_price,
            notes=order_item_request.notes
        )
        created_order_item = self.order_item_repository.create_order_item(order_item)
        return OrderItemResponse(**created_order_item.__dict__)


    def update_order_item(self, order_item_id: int, order_item_request: OrderItemRequest) -> OrderItemResponse:
        order_item_entity = self.order_item_repository.get_order_item_by_id(order_item_id)
        if not order_item_entity:
            raise OrderItemNotFoundException(order_item_id=order_item_id)

        order = self.order_repository.get_order_by_id(order_item_entity.order_id)
        if order.status in (OrderStatus.DELIVERED, OrderStatus.CANCELED):
            raise InvalidOrderItemException(order_id=order.id, status=order.status.value)

        # Update fields
        order_item_entity.quantity = order_item_request.quantity
        order_item_entity.unit_price = order_item_request.unit_price
        order_item_entity.notes = order_item_request.notes
        order_item_entity.subtotal = order_item_entity.unit_price * order_item_entity.quantity

        updated_order_item = self.order_item_repository.update_order_item(order_item_entity)
        return OrderItemResponse(**updated_order_item.__dict__)


    def get_order_item_by_id(self, order_item_id: int) -> OrderItemResponse:
        order_item_entity = self.order_item_repository.get_order_item_by_id(order_item_id)
        if not order_item_entity:
            raise OrderItemNotFoundException(order_item_id=order_item_id)
        return OrderItemResponse(**order_item_entity.__dict__)


    def list_order_items(
        self,
        order_id: int = None,
        skip: int = 0,
        limit: int = 10
    ) -> list[OrderItemResponse]:
        items = []
        if order_id is not None:
            if not self.order_repository.exists(order_id):
                raise OrderNotFoundException(order_id=order_id)
            items = self.order_item_repository.get_order_items_by_order_id(order_id)
        else:
            items = self.order_item_repository.get_all_order_items()
        items = items[skip: skip + limit] if items else []
        return [OrderItemResponse(**item.__dict__) for item in items]


    def delete_order_item(self, order_item_id: int) -> bool:
        order_item_entity = self.order_item_repository.get_order_item_by_id(order_item_id)
        if not order_item_entity:
            raise OrderItemNotFoundException(order_item_id=order_item_id)

        order = self.order_repository.get_order_by_id(order_item_entity.order_id)
        if order.status in (OrderStatus.DELIVERED, OrderStatus.CANCELED):
            raise InvalidOrderItemException(order_id=order.id, status=order.status.value)


        return self.order_item_repository.delete_order_item(order_item_id)
