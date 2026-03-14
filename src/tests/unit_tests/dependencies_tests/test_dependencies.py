#pylint: disable=unused-argument
from unittest.mock import MagicMock, patch, patch
from src.api.dependencies import (
    get_db,
    get_user_usecase,
    get_account_usecase,
    get_address_usecase,
    get_product_usecase,
    get_category_usecase,
    get_order_usecase,
    get_order_item_usecase,
    get_review_usecase,
    get_auth_usecase,
    get_current_user,
)
from src.usecases.user_usecases import UserUsecase
from src.usecases.account_usecases import AccountUsecase
from src.usecases.address_usecase import AddressUsecase
from src.usecases.product_usecases import ProductUsecase
from src.usecases.category_usecases import CategoryUsecase
from src.usecases.order_usecases import OrderUsecase
from src.usecases.order_item_usecases import OrderItemUsecase
from src.usecases.review_usecases import ReviewUsecase
from src.usecases.auth_usecases import AuthUseCases
from src.dto.response.user_response import UserResponse
import src.api.dependencies as deps

def make_fake_db():
    """Returns a mock that simulates a DBConnectionHandler."""
    fake_db = MagicMock()
    fake_db.session = MagicMock()
    return fake_db


def test_get_db_yields_db_instance():
    fake_db = MagicMock()
    with patch("src.api.dependencies.DBConnectionHandler") as MockHandler:
        MockHandler.return_value.__enter__.return_value = fake_db
        MockHandler.return_value.__exit__.return_value = False

        result = list(get_db())
        assert result == [fake_db]


def test_get_user_usecase_returns_correct_type():
    result = get_user_usecase(db=make_fake_db())
    assert isinstance(result, UserUsecase)


def test_get_account_usecase_returns_correct_type():
    result = get_account_usecase(db=make_fake_db())
    assert isinstance(result, AccountUsecase)


def test_get_address_usecase_returns_correct_type():
    result = get_address_usecase(db=make_fake_db())
    assert isinstance(result, AddressUsecase)


def test_get_product_usecase_returns_correct_type():
    result = get_product_usecase(db=make_fake_db())
    assert isinstance(result, ProductUsecase)


def test_get_category_usecase_returns_correct_type():
    result = get_category_usecase(db=make_fake_db())
    assert isinstance(result, CategoryUsecase)


def test_get_order_usecase_returns_correct_type():
    result = get_order_usecase(db=make_fake_db())
    assert isinstance(result, OrderUsecase)


def test_get_order_item_usecase_returns_correct_type():
    result = get_order_item_usecase(db=make_fake_db())
    assert isinstance(result, OrderItemUsecase)


def test_get_review_usecase_returns_correct_type():
    result = get_review_usecase(db=make_fake_db())
    assert isinstance(result, ReviewUsecase)


def test_get_auth_usecase_returns_correct_type():
    result = get_auth_usecase(db=make_fake_db())
    assert isinstance(result, AuthUseCases)


def test_get_current_user_returns_user_response():
    fake_user = MagicMock(spec=UserResponse)
    fake_token_payload = MagicMock()
    fake_token_payload.sub = "user@example.com"

    fake_user_usecase = MagicMock()
    fake_user_usecase.get_user_by_email.return_value = fake_user

    original_verify = deps.verify_token
    deps.verify_token = lambda token: fake_token_payload

    try:
        result = get_current_user(token="faketoken", user_usecase=fake_user_usecase)
        assert result == fake_user
        fake_user_usecase.get_user_by_email.assert_called_once_with("user@example.com")
    finally:
        deps.verify_token = original_verify
