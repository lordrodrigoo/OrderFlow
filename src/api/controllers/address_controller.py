import os
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, status
from src.auth.dependencies import get_current_user
from src.usecases.address_usecase import AddressUsecase
from src.infra.db.repositories.address_repository_interface import AddressRepository
from src.infra.db.settings.connection import DBConnectionHandler
from src.dto.request.address_request import AddressRequest
from src.dto.response.address_response import AddressResponse


load_dotenv()
API_PREFIX = os.getenv("API_V1_ADDRESS")
TAG = os.getenv("TAG_ADDRESS")
router = APIRouter(prefix=API_PREFIX, tags=[TAG])

db_handler = DBConnectionHandler()
address_repository = AddressRepository(db_handler)
address_usecase = AddressUsecase(address_repository)


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(address_request: AddressRequest, response: Response):
    """Endpoint to create a new address."""
    address = address_usecase.create_address(address_request)
    response.headers['Location'] = f"{API_PREFIX}/{address.id}"
    return address


@router.get("/{address_id}", response_model=AddressResponse, status_code=status.HTTP_200_OK)
def find_address_by_id(address_id: int, response: Response):
    """Endpoint to get an address by address_id."""
    address = address_usecase.find_address_by_id(address_id)
    response.headers['Location'] = f"{API_PREFIX}/{address.id}"
    return address


@router.get("/", response_model=List[AddressResponse], status_code=status.HTTP_200_OK)
def find_all_addresses() -> List[AddressResponse]:
    """Endpoint to list all addresses."""
    addresses = address_usecase.find_all_addresses()
    return addresses


@router.put(
        "/{address_id}",
        response_model=AddressResponse,
        status_code=status.HTTP_200_OK
)
def update_address(
        address_id: int,
        address_request: AddressRequest,
        current_user = Depends(get_current_user)
):
    """Endpoint to update an existing address."""
    updated_address = address_usecase.update_address(
        address_id,
        address_request,
        current_user
    )
    return updated_address



@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int):
    """Endpoint to delete an address."""
    address_usecase.delete_address(address_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/user/{user_id}", response_model=List[AddressResponse], status_code=status.HTTP_200_OK)
def find_addresses_by_user_id(user_id: int) -> List[AddressResponse]:
    """Endpoint to get addresses by user_id."""
    addresses = address_usecase.find_addresses_by_user_id(user_id)
    return addresses
