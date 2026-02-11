from fastapi import HTTPException
from src.dto.request.address_request import AddressRequest
from src.dto.response.address_response import AddressResponse
from src.domain.models.address import Address
from src.domain.repositories.address_repository import AddressRepositoryInterface
from src.domain.models.user import Users


class AddressUsecase:
    def __init__(self, address_repository: AddressRepositoryInterface):
        self.address_repository = address_repository


    def create_address(self, address_request: AddressRequest) -> AddressResponse:
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
            id=None,
            created_at=None,
            updated_at=None
        )
        created_address = self.address_repository.create_address(address_entity)
        return AddressResponse(**created_address.__dict__)


    def update_address(
            self,
            address_id: int,
            address_request: AddressRequest,
            current_user: Users
        ) -> AddressResponse:

        address = self.address_repository.find_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        if address.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this address")

        address_entity = Address(
            id=address_id,
            user_id=address_request.user_id,
            street=address_request.street,
            number=address_request.number,
            neighborhood=address_request.neighborhood,
            city=address_request.city,
            state=address_request.state,
            zip_code=address_request.zip_code,
            is_default=address_request.is_default
        )
        updated_address = self.address_repository.update_address(address_entity)
        return AddressResponse(**updated_address.__dict__)


    def find_all_addresses(self) -> list[AddressResponse]:
        addresses = self.address_repository.find_all_addresses()
        return [AddressResponse(**address.__dict__) for address in addresses]



    def find_address_by_id(self, address_id: int) -> AddressResponse:
        address = self.address_repository.find_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        return AddressResponse(**address.__dict__)


    def find_addresses_by_user_id(self, user_id: int) -> list[AddressResponse]:
        addresses = self.address_repository.find_addresses_by_user_id(user_id)
        return [AddressResponse(**address.__dict__) for address in addresses]


    def delete_address(self, address_id: int) -> bool:
        if not self.address_repository.find_address_by_id(address_id):
            raise HTTPException(status_code=404, detail="Address not found")
        return self.address_repository.delete_address(address_id)
