import os
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, Response, status, Depends
from src.api.dependencies import get_address_usecase
from src.dto.request.address_request import AddressRequest
from src.dto.response.address_response import AddressResponse


load_dotenv()
API_PREFIX = os.getenv("API_V1_ADDRESS")
TAG = os.getenv("TAG_ADDRESS")
router = APIRouter(prefix=API_PREFIX, tags=[TAG])




@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    address_request: AddressRequest,
    response: Response,
    address_usecase = Depends(get_address_usecase)
):
    """Endpoint to create a new address."""
    address = address_usecase.create_address(address_request)
    response.headers['Location'] = f"{API_PREFIX}/{address.id}"
    return address


@router.get("/{address_id}", response_model=AddressResponse, status_code=status.HTTP_200_OK)
def find_address_by_id(
    address_id: int,
    response: Response,
    address_usecase = Depends(get_address_usecase)
):
    """Endpoint to get an address by address_id."""
    address = address_usecase.find_address_by_id(address_id)
    response.headers['Location'] = f"{API_PREFIX}/{address.id}"
    return address


@router.get("/", response_model=List[AddressResponse], status_code=status.HTTP_200_OK)
def find_all_addresses(
    address_usecase = Depends(get_address_usecase)) -> List[AddressResponse]:
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
    address_usecase = Depends(get_address_usecase)
):
    """Endpoint to update an existing address."""
    updated_address = address_usecase.update_address(
        address_id,
        address_request
    )
    return updated_address



@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: int,
    address_usecase = Depends(get_address_usecase)):

    """Endpoint to delete an address."""
    address_usecase.delete_address(address_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/user/{user_id}", response_model=List[AddressResponse], status_code=status.HTTP_200_OK)
def find_addresses_by_user_id(
    user_id: int,
    address_usecase = Depends(get_address_usecase)
)-> List[AddressResponse]:

    """Endpoint to get addresses by user_id."""
    addresses = address_usecase.find_addresses_by_user_id(user_id)
    return addresses
