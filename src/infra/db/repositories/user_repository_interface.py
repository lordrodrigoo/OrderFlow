from typing import List, Optional
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.user import UserEntity
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.domain.models.user import Users, UserRole
from src.infra.db.repositories.base_repository import BaseRepository


class UserRepository(UserRepositoryInterface, BaseRepository[UserEntity]):
    def __init__(self, db_connection: DBConnectionHandler):
        super().__init__(db_connection.get_session(), UserEntity)

    def create_user(self, user: Users) -> Users:
        entity = UserEntity(
            first_name=user.first_name,
            last_name=user.last_name,
            age=user.age,
            email=user.email,
            phone=user.phone,
            is_active=user.is_active,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.add(entity)
        self.save()
        return Users.from_entity(entity)

    def update_user(self, user: Users) -> Users:
        entity = self.get_by_id(user.id)
        if entity:
            entity.first_name = user.first_name
            entity.last_name = user.last_name
            entity.age = user.age
            entity.email = user.email
            entity.phone = user.phone
            entity.is_active = user.is_active
            entity.role = user.role.value
            entity.updated_at = user.updated_at
            self.save()
        return Users.from_entity(entity)


    def get_user_by_role(self, role: UserRole) -> List[Users]:
        entities = self.session.query(self.model).filter(self.model.role == role.value).all()
        return [Users.from_entity(user) for user in entities]

    def is_admin(self, user_id: int) -> bool:
        entity = self.get_by_id(user_id)
        return entity.role == UserRole.ADMIN.value if entity else False

    def find_all_users(self) -> List[Users]:
        return [Users.from_entity(user) for user in self.get_all()]

    def find_user_by_id(self, user_id: int) -> Optional[Users]:
        entity = self.get_by_id(user_id)
        return Users.from_entity(entity) if entity else None

    def find_by_email(self, email: str) -> Optional[Users]:
        entity = self.session.query(self.model).filter(self.model.email == email).first()
        return Users.from_entity(entity) if entity else None

    def find_by_name(self, name: str) -> List[Users]:
        entities = self.session.query(self.model).filter(self.model.first_name == name).all()
        return [Users.from_entity(user) for user in entities]

    def delete_user(self, user_id: int) -> bool:
        entity = self.get_by_id(user_id)

        if entity:
            self.delete(entity)
            self.save()
            return True
        return False
