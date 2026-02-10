from fastapi import HTTPException
from src.dto.request.address_request import AddressRequest
from src.dto.response.address_response import AddressResponse
from src.domain.models.address import Address
from src.domain.repositories.address_repository import AddressRepositoryInterface



class AddressUsecase:
    def __init__(self, address_repository: AddressRepositoryInterface):
        self.address_repository = address_repository


    def create_address(self, address_request: AddressRequest) -> AddressResponse:
        if self.address_repository.find_address_by_id(address_request.id):
            raise HTTPException(status_code=409, detail="Address already exists")

        address_entity = Address(
            user_id=address_request.user_id,
            street=address_request.street,
            city=address_request.city,
            state=address_request.state,
            zip_code=address_request.zip_code,
            country=address_request.country
        )
        created_address = self.address_repository.create_address(address_entity)
        return AddressResponse(**created_address.__dict__)
