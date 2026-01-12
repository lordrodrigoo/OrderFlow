from typing import List
from datetime import datetime
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.user import User as UserEntity
from src.data.interfaces.user_repository import UserRepositoryInterface
from src.domain.models.user import Users


class UserRepository(UserRepositoryInterface):

    @classmethod
    def insert_user(
        cls,
        first_name: str,
        last_name: str,
        password_hash: str,
        age: int,
        phone: str,
        email: str,
        is_active: bool,
        created_at: datetime,
        updated_at: datetime
    ) -> Users:
        with DBConnectionHandler() as db_connection:
            try:
                new_registry = UserEntity(
                    first_name=first_name,
                    last_name=last_name,
                    password_hash=password_hash,
                    age=age,
                    phone=phone,
                    email=email,
                    is_active=is_active,
                    created_at=created_at,
                    updated_at=updated_at
                )
                db_connection.session.add(new_registry)
                db_connection.session.commit()
            except Exception as exception:
                db_connection.session.rollback()
                raise exception

    @classmethod
    def select_user(cls, first_name: str) -> List[Users]:
        with DBConnectionHandler() as db_connection:
            try:
                users = (
                    db_connection.session
                    .query(UserEntity)
                    .filter(UserEntity.first_name == first_name)
                    .all()
                )
                return users
            except Exception as exception:
                db_connection.session.rollback()
                raise exception
