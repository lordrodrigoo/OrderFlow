from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base



class ProductEntity(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    preparation_time_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now())

    "Bellow are foreign keys and relationships"
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('CategoryEntity', back_populates='products')
    order_items = relationship('OrderItemEntity', back_populates='product')
    reviews = relationship('ReviewEntity', back_populates='product')

    def __repr__(self):
        return f"Product [id = {self.id}, name = {self.name}, price = {self.price}, category_id = {self.category_id}]"
