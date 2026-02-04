from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base



class UserEntity(Base):
    """Entity class representing the users table in the database."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now())

    accounts = relationship('AccountEntity', back_populates='user')
    addresses = relationship('AddressEntity', back_populates='user')
    orders = relationship('OrderEntity', back_populates='user')
    reviews = relationship('ReviewEntity', back_populates='user')

    def __repr__(self):
        return (
            f"UserEntity(id={self.id}, first_name='{self.first_name}', "
            f"last_name='{self.last_name}', email='{self.email}')"
        )
