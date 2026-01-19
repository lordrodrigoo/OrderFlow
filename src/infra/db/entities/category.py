from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from src.infra.db.settings.base import Base

class CategoryEntity(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)

    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"CategoryEntity [id = {self.id}, name = {self.name}]"
