from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base



class OrderEntity(Base):
    __tablename__ = 'orders'


    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    delivery_fee = Column(Numeric(10, 2), nullable=False)
    notes = Column(String(255), nullable=True)
    scheduled_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)

    user = relationship('UserEntity', back_populates='orders')
    order_items = relationship('OrderItemEntity', back_populates='order')
    review = relationship('ReviewEntity', back_populates='order', uselist=False)

    def __repr__(self):
        return f"Order [id = {self.id}, user_id = {self.user_id}, total_amount = {self.total_amount}, status = {self.status}]"
