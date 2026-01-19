from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base

class OrderEntity(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    "Bellow are foreign keys and relationships"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='orders')
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    address = relationship('Address', backref='orders')
    order_items = relationship('OrderItem', backref='order')
    review = relationship('Review', backref='order', uselist=False)


    def __repr__(self):
        return f"Order [id = {self.id}, user_id = {self.user_id}, total_amount = {self.total_amount}, status = {self.status}]"
