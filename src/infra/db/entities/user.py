from sqlalchemy import Column, Integer, String
from src.infra.db.settings.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(128), nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(bool, default=True)
    created_at = Column(String(30), nullable=False)
    updated_at = Column(String(30), nullable=True)

    def __repr__(self):
        return f"Users [id = {self.id}, first_name = {self.first_name}, last_name =    {self.last_name}, phone = {self.phone}, email = {self.email}]"
