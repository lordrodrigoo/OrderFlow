from typing import Optional, List
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.address import AddressEntity
from src.domain.repositories.address_repository import AddressRepositoryInterface
from src.domain.models.address import Address
from src.infra.db.repositories.base_repository import BaseRepository



class AddressRepository(AddressRepositoryInterface, BaseRepository[AddressEntity]):
    def __init__(self, db_connection: DBConnectionHandler):
        super().__init__(db_connection.get_session(), AddressEntity)

    def create_address(self, address: Address) -> Address:
        entity = AddressEntity(
            user_id=address.user_id,
            street=address.street,
            number=address.number,
            complement=address.complement,
            neighborhood=address.neighborhood,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            is_default=address.is_default,
            created_at=address.created_at,
            updated_at=address.updated_at
        )
        self.add(entity)
        self.save()
        return Address.from_entity(entity)

    def update_address(self, address: Address) -> Address:
        entity = self.get_by_id(address.id)

        if entity:
            entity.user_id = address.user_id
            entity.street = address.street
            entity.number = address.number
            entity.complement = address.complement
            entity.neighborhood = address.neighborhood
            entity.city = address.city
            entity.state = address.state
            entity.zip_code = address.zip_code
            entity.is_default = address.is_default
            entity.updated_at = address.updated_at
            self.save()

        return Address.from_entity(entity)

    def find_all_addresses(self) -> List[Address]:
        return [Address.from_entity(address) for address in self.get_all()]

    def find_address_by_id(self, address_id: int) -> Optional[Address]:
        entity = self.get_by_id(address_id)
        return Address.from_entity(entity) if entity else None

    def find_by_zip_code(self, zip_code: str) -> List[Address]:
        entities = self.session.query(self.model).filter(self.model.zip_code == zip_code).all()
        return [Address.from_entity(address) for address in entities]

    def delete_address(self, address_id: int) -> bool:
        return self.delete_by_id(address_id)

    def find_addresses_by_user_id(self, user_id: int) -> List[Address]:
        entities = self.session.query(
            self.model).filter(self.model.user_id == user_id).all()
        return [Address.from_entity(address) for address in entities]


    def find_addresses_by_user_street_number(
        self,
        user_id: int,
        street: str,
        number: str
    ) -> List[Address]:
        entities = self.session.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.street == street,
            self.model.number == number
        ).all()
        return [Address.from_entity(address) for address in entities]


    def set_default_address(self, address_id: int, user_id: int) -> Optional[Address]:
        # First, unset the current default address for the user
        self.session.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.is_default is True
        ).update({self.model.is_default: False})

        # After that, set the specified address as default
        entity = self.get_by_id(address_id)
        if entity and entity.user_id == user_id:
            entity.is_default = True
            self.save()
            return Address.from_entity(entity)

        return None
