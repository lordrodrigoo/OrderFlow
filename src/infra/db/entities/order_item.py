from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base


class OrderItemEntity(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    "Bellow are foreign keys and relationships"
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    order = relationship('OrderEntity', back_populates='order_items')
    product = relationship('ProductEntity', back_populates='order_items')

    def __repr__(self):
        return f"OrderItem [id = {self.id}, order_id = {self.order_id}, product_id = {self.product_id}, quantity = {self.quantity}]"
