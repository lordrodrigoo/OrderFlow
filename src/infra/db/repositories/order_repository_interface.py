from typing import List
from decimal import Decimal
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.order import OrderEntity
from src.domain.repositories.order_repository import OrderRepositoryInterface
from src.domain.models.order import Order
from src.infra.db.repositories.base_repository import BaseRepository


class OrderRepository(OrderRepositoryInterface, BaseRepository[OrderEntity]):
    def __init__(self, db_connection: DBConnectionHandler):
        super().__init__(db_connection.get_session(), OrderEntity)

    def create_order(self, order: Order) -> Order:
        entity = OrderEntity(
            status = order.status,
            total_amount = order.total_amount,
            delivery_fee = order.delivery_fee,
            notes = order.notes,
            scheduled_date = order.scheduled_date,
            created_at = order.created_at,
            updated_at = order.updated_at,
        )
        self.add(entity)
        self.save()
        return Order.from_entity(entity)

    def update_order(self, order: Order) -> Order:
        entity = self.get_by_id(order.id)
        if entity:
            entity.status = order.status
            entity.total_amount = order.total_amount
            entity.delivery_fee = order.delivery_fee
            entity.notes = order.notes
            entity.scheduled_date = order.scheduled_date
            entity.updated_at = order.updated_at
            self.save()
        return Order.from_entity(entity)

    def get_all_orders(self) -> List[Order]:
        return [Order.from_entity(order) for order in self.get_all()]

    def find_orders_by_status(self, status: str) -> List[Order]:
        entities = self.session.query(self.model).filter(self.model.status == status).all()
        return [Order.from_entity(order) for order in entities]

    def find_orders_by_user(self, user_id: int) -> List[Order]:
        entities = self.session.query(self.model).filter(self.model.user_id == user_id).all()
        return [Order.from_entity(order) for order in entities]

    def get_order_by_id(self, order_id: int) -> Order | None:
        entity = self.get_by_id(order_id)
        if entity:
            return Order.from_entity(entity)
        return None

    def find_orders_by_total_amount(self, min_amount: Decimal, max_amount: Decimal)-> List[Order]:
        entities = self.session.query(
            self.model).filter(self.model.total_amount.between(min_amount, max_amount)).all()
        return [Order.from_entity(order) for order in entities]

    def cancel_order(self, order_id: int) -> bool:
        entity = self.get_by_id(order_id)
        if entity:
            entity.status = 'canceled'
            self.save()
            return True
        return False

    def delete_order(self, order_id: int) -> bool:
        entity = self.get_by_id(order_id)
        if entity:
            self.delete(entity)
            self.save()
            return True
        return False
