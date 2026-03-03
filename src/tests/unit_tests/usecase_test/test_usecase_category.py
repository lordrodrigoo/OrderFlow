#pylint: disable=unused-argument
import pytest
from pydantic import ValidationError
from src.domain.models.category import Category
from src.dto.request.category_request import CategoryRequest
from src.dto.response.category_response import CategoryResponse
from src.exceptions.exception_handlers_category import (
    CategoryAlreadyExistsException,
    CategoryNotFoundException
)



def test_create_category(
        category_usecase,
        category_repository_mock,
        valid_category_request
    ):
    category_repository_mock.find_category_by_name.return_value = None
    response = category_usecase.create_category(valid_category_request)

    assert isinstance(response, CategoryResponse)
    assert response.name == valid_category_request.name
    assert response.description == valid_category_request.description


def test_create_category_with_existing_name(
        category_usecase,
        category_repository_mock,
        valid_category_request
    ):
    category_repository_mock.find_category_by_name.return_value = Category(
        id=1,
        name=valid_category_request.name,
        description=valid_category_request.description
    )

    with pytest.raises(CategoryAlreadyExistsException):
        category_usecase.create_category(valid_category_request)


def test_create_category_with_invalid_data():
    with pytest.raises(ValidationError) as exc_info:
        CategoryRequest(
            name="",  # Invalid name, should not be empty
            description="Categoria de pizzas deliciosas"
        )
    assert "String should have at least 3 characters" in str(exc_info.value)


def test_update_category(
        category_usecase,
        category_repository_mock,
        valid_category_request
    ):
    existing = Category(id=1, name="Old Name", description="Old Description")
    updated = Category(id=1, name=valid_category_request.name, description=valid_category_request.description)

    category_repository_mock.get_category_by_id.return_value = existing
    category_repository_mock.find_category_by_name.return_value = updated
    category_repository_mock.update_category.return_value = updated
    response = category_usecase.update_category(1, valid_category_request)

    assert isinstance(response, CategoryResponse)
    assert response.name == valid_category_request.name
    assert response.description == valid_category_request.description


def test_update_category_not_found(
        category_usecase,
        category_repository_mock,
        valid_category_request
    ):
    category_repository_mock.get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFoundException):
        category_usecase.update_category(999, valid_category_request)


def test_update_category_with_existing_name(
        category_usecase,
        category_repository_mock,
        valid_category_request
    ):
    conflicting = Category(id=2, name=valid_category_request.name, description="Outra descrição")
    category_repository_mock.get_category_by_id.return_value = conflicting
    category_repository_mock.find_category_by_name.return_value = conflicting

    with pytest.raises(CategoryAlreadyExistsException):
        category_usecase.update_category(1, valid_category_request)


def test_get_category_by_id(
        category_usecase,
        category_repository_mock
    ):
    category_repository_mock.get_category_by_id.return_value = Category(
        id=1,
        name="Pizzas",
        description="Categoria de pizzas deliciosas"
    )
    response = category_usecase.get_category_by_id(1)

    assert isinstance(response, CategoryResponse)
    assert response.id == 1
    assert response.name == "Pizzas"
    assert response.description == "Categoria de pizzas deliciosas"



def test_get_category_by_id_not_found(
        category_usecase,
        category_repository_mock
    ):
    category_repository_mock.get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFoundException):
        category_usecase.get_category_by_id(999)


def test_list_all_categories(
        category_usecase,
        category_repository_mock
    ):

    category_repository_mock.get_all_categories.return_value = [
        Category(id=1, name="Pizzas", description="Categoria de pizzas deliciosas"),
        Category(id=2, name="Bebidas", description="Categoria de bebidas refrescantes")
    ]
    response = category_usecase.list_categories()

    assert isinstance(response, list)
    assert len(response) == 2
    assert response[0].name == "Pizzas"
    assert response[1].name == "Bebidas"


def test_list_categories_empty(
        category_usecase,
        category_repository_mock
    ):
    category_repository_mock.get_all_categories.return_value = []
    response = category_usecase.list_categories()

    assert isinstance(response, list)
    assert len(response) == 0


def test_delete_category(
        category_usecase,
        category_repository_mock
    ):
    category_repository_mock.get_category_by_id.return_value = Category(
        id=1,
        name="Pizzas",
        description="Categoria de pizzas deliciosas"
    )
    category_repository_mock.delete_category.return_value = True
    result = category_usecase.delete_category(1)
    assert result is True


def test_delete_category_not_found(
        category_usecase,
        category_repository_mock
    ):
    category_repository_mock.get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFoundException):
        category_usecase.delete_category(999)
