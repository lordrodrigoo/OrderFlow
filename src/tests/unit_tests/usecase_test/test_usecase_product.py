#pylint: disable=unused-argument
from decimal import Decimal
from datetime import datetime
import pytest
from pydantic import ValidationError
from src.dto.request.product_request import ProductRequest
from src.dto.response.product_response import ProductResponse
from src.exceptions.exception_handlers_product import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    ProductCategoryNotFoundException,
    InvalidPriceProductException
)



def test_create_product(
        product_usecase,
        fake_product_repository_mock,
        category_repository_mock,
        valid_product_data
    ):
    request = ProductRequest(**valid_product_data)
    response = product_usecase.create_product(request)

    assert isinstance(response, ProductResponse)
    assert response.name == valid_product_data["name"]
    assert response.description == valid_product_data["description"]
    assert response.price == Decimal(str(valid_product_data["price"]))
    assert response.is_available == valid_product_data["is_available"]
    assert response.preparation_time == valid_product_data["preparation_time"]


def test_product_already_exists(
        product_usecase,
        fake_product_repository_mock,
        category_repository_mock,
        valid_product_data
    ):
    fake_product_repository_mock.find_products_by_name.return_value = [ProductResponse(**{
        "id": 1,
        **valid_product_data,
        "created_at": datetime.now()
    })]
    request = ProductRequest(**valid_product_data)
    with pytest.raises(ProductAlreadyExistsException) as exc_info:
        product_usecase.create_product(request)
    assert valid_product_data["name"] in exc_info.value.message


def test_product_category_not_found(
        product_usecase,
        fake_product_repository_mock,
        category_repository_mock,
        valid_product_data
    ):
    category_repository_mock.get_category_by_id.return_value = None
    request = ProductRequest(**valid_product_data)
    with pytest.raises(ProductCategoryNotFoundException) as exc_info:
        product_usecase.create_product(request)
    assert str(valid_product_data["category_id"]) in exc_info.value.message


def test_product_invalid_price(
        product_usecase,
        fake_product_repository_mock,
        category_repository_mock,
        valid_product_data
    ):
    request = ProductRequest(**{**valid_product_data, "price": 0})
    with pytest.raises(InvalidPriceProductException):
        product_usecase.create_product(request)


def test_update_product(
        product_usecase,
        fake_product_repository_mock,
        category_repository_mock,
        valid_product_data,
        fake_product_response_mock
    ):

    fake_product_repository_mock.find_product_by_id.return_value = fake_product_response_mock
    # Creating a request object with updated data
    update_data = {
        "name": "Pizza Pepperoni",
        "description": "Deliciosa pizza com molho de tomate, mussarela e pepperoni",
        "category_id": 1,
        "price": 34.90,
        "is_available": True,
        "preparation_time": 25
    }
    request = ProductRequest(**update_data)
    fake_product_repository_mock.update_product.return_value = ProductResponse(**{
        **update_data,
        "id": 1,
        "created_at": datetime.now()
    })
    response = product_usecase.update_product(1, request)

    assert response.name == update_data["name"]
    assert response.description == update_data["description"]
    assert response.price == Decimal(str(update_data["price"]))
    assert response.is_available == update_data["is_available"]
    assert response.preparation_time == update_data["preparation_time"]


def test_product_invalid_request():
    with pytest.raises(ValidationError):
        ProductRequest(
            name="",
            description="",
            category_id=1,
            price=-10.00,
            is_available=True,
            preparation_time=-5
        )


def test_find_all_products(
        product_usecase,
        fake_product_repository_mock,
        category_repository_mock,
        fake_product_response_mock
    ):
    fake_product_repository_mock.get_all_products.return_value = [fake_product_response_mock]
    response = product_usecase.list_products()

    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0].name == fake_product_response_mock.name
    assert response[0].description == fake_product_response_mock.description
    assert response[0].price == fake_product_response_mock.price
    assert response[0].is_available == fake_product_response_mock.is_available
    assert response[0].preparation_time == fake_product_response_mock.preparation_time


def test_get_product_by_id(
        product_usecase,
        fake_product_repository_mock,
        category_repository_mock,
        fake_product_response_mock
    ):
    fake_product_repository_mock.find_product_by_id.return_value = fake_product_response_mock
    response = product_usecase.get_product_by_id(1)

    assert response.name == fake_product_response_mock.name
    assert response.description == fake_product_response_mock.description
    assert response.price == fake_product_response_mock.price
    assert response.is_available == fake_product_response_mock.is_available
    assert response.preparation_time == fake_product_response_mock.preparation_time


def test_get_product_by_id_not_found(
        product_usecase,
        fake_product_repository_mock,
        category_repository_mock
    ):
    fake_product_repository_mock.find_product_by_id.return_value = None
    with pytest.raises(ProductNotFoundException):
        product_usecase.get_product_by_id(999)
