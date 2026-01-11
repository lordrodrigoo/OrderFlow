from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    preparation_time_minutes = Column(Integer, nullable=True)
    created_at = Column(String(30), nullable=False)
    updated_at = Column(String(30), nullable=True)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category', backref='products')

    def __repr__(self):
        return f"Product [id = {self.id}, name = {self.name}, price = {self.price}, category_id = {self.category_id}]"
