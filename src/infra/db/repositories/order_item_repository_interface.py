from typing import List
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.order_item import OrderItemEntity
from src.domain.repositories.order_item_repository import OrderItemRepositoryInterface
from src.domain.models.order_item import OrderItem
from src.infra.db.repositories.base_repository import BaseRepository


class OrderItemRepository(OrderItemRepositoryInterface, BaseRepository[OrderItemEntity]):
    def __init__(self, db_connection: DBConnectionHandler):
        super().__init__(db_connection.get_session(), OrderItemEntity)

    def create_order_item(self, order_item: OrderItem) -> OrderItem:
        entity = OrderItemEntity(
            order_id = order_item.order_id,
            product_id = order_item.product_id,
            quantity = order_item.quantity,
            unit_price = order_item.unit_price,
            subtotal = order_item.subtotal,
            notes = order_item.notes,
        )
        self.add(entity)
        self.save()
        return OrderItem.from_entity(entity)

    def update_order_item(self, order_item: OrderItem) -> OrderItem:
        entity = self.get_by_id(order_item.id)
        if entity:
            entity.order_id = order_item.order_id
            entity.product_id = order_item.product_id
            entity.quantity = order_item.quantity
            entity.unit_price = order_item.unit_price
            entity.subtotal = order_item.subtotal
            entity.notes = order_item.notes
            self.save()
        return OrderItem.from_entity(entity)

    def get_all_order_items(self) -> List[OrderItem]:
        return [OrderItem.from_entity(item) for item in self.get_all()]

    def get_order_item_by_id(self, order_item_id: int) -> OrderItem | None:
        entity =  self.get_by_id(order_item_id)
        if entity:
            return OrderItem.from_entity(entity)
        return None

    def delete_order_item(self, order_item_id: int) -> bool:
        return self.delete_by_id(order_item_id)
