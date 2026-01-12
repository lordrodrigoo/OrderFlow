from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base
from src.infra.db.entities.user import User  #pylint: disable=unused-import


class Address(Base):
    __tablename__= 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    street = Column(String(100), nullable=False)
    number = Column(String(10), nullable=False)
    complement = Column(String(50), nullable=True)
    neighborhood = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    user = relationship('User', backref='addresses')

    def __repr__(self):
        return f"Address [id = {self.id}, user_id = {self.user_id}, street = {self.street}, city = {self.city}]"
