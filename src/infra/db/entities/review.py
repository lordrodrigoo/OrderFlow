from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base


class ReviewEntity(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Numeric(2, 1), nullable=False)
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())


    "Bellow are foreign keys and relationships"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('UserEntity', back_populates='reviews')
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('ProductEntity', back_populates='reviews')

    def __repr__(self):
        return f"Review [id = {self.id}, rating = {self.rating}]"
