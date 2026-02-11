#pylint: disable=unused-argument
from datetime import datetime
import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from src.dto.request.address_request import AddressRequest
from src.dto.response.address_response import AddressResponse


def test_create_address(
        address_usecase,
        fake_address_repository_mock,
        valid_address_data
    ):
    request = AddressRequest(**valid_address_data)
    response = address_usecase.create_address(request)

    assert isinstance(response, AddressResponse)
    assert response.street ==valid_address_data["street"]
    assert response.city == valid_address_data["city"]
    assert response.state == valid_address_data["state"]
    assert response.zip_code == valid_address_data["zip_code"]


def test_update_address(
        address_usecase,
        fake_address_repository_mock,
        valid_address_data,
        fake_address_response_mock,
        fake_user
    ):

    fake_address_repository_mock.find_address_by_id.return_value = fake_address_response_mock
    # Creating a request object with updated data
    update_data = {
        "user_id": 1,
        "street": "rua Ipiranga",
        "number": "456",
        "neighborhood": "Centro",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "03433023",
        "is_default": True,
        "complement": "casa 2 fundos"
    }
    request = AddressRequest(**update_data)
    fake_address_repository_mock.update_address.return_value = AddressResponse(**{
        **update_data,
        "id": 1,
        "created_at": datetime.now()
    })
    response = address_usecase.update_address(1, request, fake_user)

    assert response.street == update_data["street"]
    assert response.city == update_data["city"]
    assert response.state == update_data["state"]
    assert response.zip_code == update_data["zip_code"]
    assert response.complement == update_data["complement"]


def test_address_invalid_request():
    with pytest.raises(ValidationError):
        AddressRequest(
            user_id=1,
            street="ok",
            number="456",
            neighborhood="Centro",
            city="São Paulo",
            state="XX",  # Invalid State
            zip_code="03433023",
            is_default=True,
            complement="casa 2 fundos"
    )


def test_find_all_addresses(
        address_usecase,
        fake_address_repository_mock,
        fake_address_response_mock
        ):
    fake_address_repository_mock.find_all_addresses.return_value = [fake_address_response_mock]
    response = address_usecase.find_all_addresses()

    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], AddressResponse)
    assert response[0].street == fake_address_response_mock.street


def test_find_address_by_id(
        address_usecase,
        fake_address_repository_mock,
        fake_address_response_mock
    ):
    fake_address_repository_mock.find_address_by_id.return_value = fake_address_response_mock
    response = address_usecase.find_address_by_id(1)
    assert isinstance(response, AddressResponse)
    assert response.id == fake_address_response_mock.id
    assert response.street == fake_address_response_mock.street
    assert response.city == fake_address_response_mock.city


def test_find_address_by_id_not_found(
        address_usecase,
        fake_address_repository_mock
    ):
    fake_address_repository_mock.find_address_by_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        address_usecase.find_address_by_id(999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Address not found"



def test_update_address_not_found(
        address_usecase,
        fake_address_repository_mock,
        valid_address_data,
        fake_user
    ):
    fake_address_repository_mock.find_address_by_id.return_value = None
    request = AddressRequest(**valid_address_data)
    with pytest.raises(HTTPException) as exc_info:
        address_usecase.update_address(999, request, fake_user)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Address not found"


def test_delete_address_not_found(
        address_usecase,
        fake_address_repository_mock
    ):
    fake_address_repository_mock.find_address_by_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        address_usecase.delete_address(999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Address not found"


def test_delete_address(
        address_usecase,
        fake_address_repository_mock,
        fake_address_response_mock
    ):
    fake_address_repository_mock.find_address_by_id.return_value = fake_address_response_mock
    fake_address_repository_mock.delete_address.return_value = True
    result = address_usecase.delete_address(1)
    assert result is True
