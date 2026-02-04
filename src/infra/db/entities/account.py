from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base



class AccountEntity(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now())

    user = relationship('UserEntity', back_populates='accounts')

    def __repr__(self):
        return (
            f"AccountEntity(id={self.id}, user_id={self.user_id}, username='{self.username}', "
            f"status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})"
        )
