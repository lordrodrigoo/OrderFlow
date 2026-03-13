from fastapi import Depends

from src.infra.db.settings.connection import DBConnectionHandler
from src.usecases.auth_usecases import AuthUseCases
from src.usecases.user_usecases import UserUsecase
from src.usecases.account_usecases import AccountUsecase
from src.usecases.address_usecase import AddressUsecase
from src.usecases.product_usecases import ProductUsecase
from src.usecases.category_usecases import CategoryUsecase
from src.usecases.order_usecases import OrderUsecase
from src.usecases.order_item_usecases import OrderItemUsecase
from src.usecases.review_usecases import ReviewUsecase
from src.infra.db.repositories.user_repository_interface import UserRepository
from src.infra.db.repositories.account_user_repository_interface import AccountRepository
from src.infra.db.repositories.address_repository_interface import AddressRepository
from src.infra.db.repositories.product_repository_interface import ProductRepository
from src.infra.db.repositories.category_repository_interface import CategoryRepository
from src.infra.db.repositories.order_repository_interface import OrderRepository
from src.infra.db.repositories.order_item_repository_interface import OrderItemRepository
from src.infra.db.repositories.review_repository_interface import ReviewRepository

from src.config.oauth2 import oauth2_scheme
from src.config.security import verify_token, TokenPayload
from src.dto.response.user_response import UserResponse





def get_db():
    with DBConnectionHandler() as db:
        yield db


def get_user_usecase(db=Depends(get_db)):
    user_repository = UserRepository(db)
    account_repository = AccountRepository(db)
    return UserUsecase(user_repository, account_repository)


def get_account_usecase(db=Depends(get_db)):
    account_repository = AccountRepository(db)
    user_repository = UserRepository(db)
    return AccountUsecase(account_repository, user_repository)


def get_address_usecase(db=Depends(get_db)):
    address_repository = AddressRepository(db)
    return AddressUsecase(address_repository)


def get_product_usecase(db=Depends(get_db)):
    product_repository = ProductRepository(db)
    category_repository = CategoryRepository(db)
    return ProductUsecase(product_repository, category_repository)


def get_category_usecase(db=Depends(get_db)):
    category_repository = CategoryRepository(db)
    return CategoryUsecase(category_repository)


def get_order_usecase(db=Depends(get_db)):
    order_repository = OrderRepository(db)
    return OrderUsecase(order_repository)


def get_order_item_usecase(db=Depends(get_db)):
    order_item_repository = OrderItemRepository(db)
    product_repository = ProductRepository(db)
    order_repository = OrderRepository(db)
    return OrderItemUsecase(order_item_repository, product_repository, order_repository)


def get_review_usecase(db=Depends(get_db)):
    review_repository = ReviewRepository(db)
    user_repository = UserRepository(db)
    product_repository = ProductRepository(db)
    return ReviewUsecase(review_repository, user_repository, product_repository)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_usecase: UserUsecase = Depends(get_user_usecase)
) -> UserResponse:
    token_data: TokenPayload = verify_token(token)
    return user_usecase.get_user_by_email(token_data.sub)


def get_auth_usecase(db=Depends(get_db)):
    account_repository = AccountRepository(db)
    user_repository = UserRepository(db)
    return AuthUseCases(account_repository, user_repository)
