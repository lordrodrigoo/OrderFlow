from typing import List
from datetime import datetime
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.address import Address as AddressEntity
from src.data.interfaces.address_repository import AddressRepositoryInterface
from src.domain.models.address import Address

class AddressRepository(AddressRepositoryInterface):

    @classmethod
    def insert_address(
        cls,
        street: str,
        number: str,
        complement: str,
        neighborhood: str,
        city: str,
        state: str,
        zip_code: str,
        is_default: bool,
        created_at: datetime,
        updated_at: datetime
    ) -> Address:
        with DBConnectionHandler() as db_connection:
            try:
                new_registry = AddressEntity(
                    street = street,
                    number = number,
                    complement = complement,
                    neighborhood = neighborhood,
                    city = city,
                    state = state,
                    zip_code = zip_code,
                    is_default = is_default,
                    created_at = created_at,
                    updated_at = updated_at
                )
                db_connection.session.add(new_registry)
                db_connection.session.commit()
            except Exception as exception:
                db_connection.session.rollback()
                raise exception

    @classmethod
    def select_address(cls, street: str) -> List[Address]:
        with DBConnectionHandler() as db_connection:
            try:
                addresses = (
                    db_connection.session
                    .query(AddressEntity)
                    .filter(AddressEntity.street == street)
                    .all()
                )
                return addresses
            except Exception as exception:
                db_connection.session.rollback()
                raise exception
