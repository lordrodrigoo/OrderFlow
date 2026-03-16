import logging
from src.dto.request.address_request import AddressRequest
from src.dto.response.address_response import AddressResponse
from src.domain.models.address import Address
from src.domain.repositories.address_repository import AddressRepositoryInterface
from src.domain.models.user import Users
from src.exceptions.exception_handlers_address import (
    AddressNotFoundException,
    AddressAlreadyExistsException,
    AddressPermissionDeniedException
)

logger = logging.getLogger(__name__)


class AddressUsecase:
    def __init__(self, address_repository: AddressRepositoryInterface):
        self.address_repository = address_repository


    def create_address(self, address_request: AddressRequest) -> AddressResponse:
        if self.address_repository.find_addresses_by_user_street_number(
            address_request.user_id,
            address_request.street,
            address_request.number
            ):
            logger.warning("Address already exists", extra={"street": address_request.street})
            raise AddressAlreadyExistsException(address=address_request.street)

        address_entity = Address(
            user_id=address_request.user_id,
            street=address_request.street,
            number=address_request.number,
            neighborhood=address_request.neighborhood,
            city=address_request.city,
            state=address_request.state,
            zip_code=address_request.zip_code,
            is_default=address_request.is_default,
            complement=address_request.complement,
        )
        created_address = self.address_repository.create_address(address_entity)
        logger.info("Address created", extra={"address_id": created_address.id})
        return AddressResponse(**created_address.__dict__)


    def update_address(
            self,
            address_id: int,
            address_request: AddressRequest,
            current_user: Users
        ) -> AddressResponse:

        address = self.address_repository.find_address_by_id(address_id)
        if not address:
            logger.warning("Address not found", extra={"address_id": address_id})
            raise AddressNotFoundException(address_id=address_id)

        if address.user_id != current_user.id:
            logger.warning("Permission denied to update address", extra={"address_id": address_id})
            raise AddressPermissionDeniedException(address_id=address_id)

        address_entity = Address(
            id=address_id,
            user_id=address_request.user_id,
            street=address_request.street,
            number=address_request.number,
            neighborhood=address_request.neighborhood,
            city=address_request.city,
            state=address_request.state,
            zip_code=address_request.zip_code,
            is_default=address_request.is_default,
            complement=address_request.complement,
        )
        updated_address = self.address_repository.update_address(address_entity)
        logger.info("Address updated", extra={"address_id": address_id})
        return AddressResponse(**updated_address.__dict__)


    def find_all_addresses(self) -> list[AddressResponse]:
        addresses = self.address_repository.find_all_addresses()
        return [AddressResponse(**address.__dict__) for address in addresses]



    def find_address_by_id(self, address_id: int) -> AddressResponse:
        address = self.address_repository.find_address_by_id(address_id)
        if not address:
            raise AddressNotFoundException(address_id=address_id)
        return AddressResponse(**address.__dict__)


    def find_addresses_by_user_id(self, user_id: int) -> list[AddressResponse]:
        if not self.address_repository.find_addresses_by_user_id(user_id):
            raise AddressNotFoundException(address_id=user_id)

        addresses = self.address_repository.find_addresses_by_user_id(user_id)
        return [AddressResponse(**address.__dict__) for address in addresses]


    def delete_address(self, address_id: int, current_user: Users) -> bool:
        address = self.address_repository.find_address_by_id(address_id)
        if not address:
            logger.warning("Address not found for deletion", extra={"address_id": address_id})
            raise AddressNotFoundException(address_id=address_id)

        if address.user_id != current_user.id:
            logger.warning("Permission denied to delete address", extra={"address_id": address_id})
            raise AddressPermissionDeniedException(address_id=address_id)
        logger.info("Address deleted", extra={"address_id": address_id})
        return self.address_repository.delete_address(address_id)


    def set_default_address(self, address_id: int, user_id: int) -> AddressResponse:
        address = self.address_repository.set_default_address(address_id, user_id)
        if not address:
            raise AddressNotFoundException(address_id=address_id)
        return AddressResponse(**address.__dict__)
