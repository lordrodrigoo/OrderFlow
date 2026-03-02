from fastapi import Depends
from src.infra.db.settings.connection import DBConnectionHandler
from src.usecases.user_usecases import UserUsecase
from src.infra.db.repositories.user_repository_interface import UserRepository
from src.infra.db.repositories.account_user_repository_interface import AccountRepository
from src.usecases.account_usecases import CreateAccountUsecase
from src.usecases.address_usecase import AddressUsecase
from src.infra.db.repositories.address_repository_interface import AddressRepository
from src.infra.db.repositories.product_repository_interface import ProductRepository
from src.usecases.product_usecases import ProductUsecase
from src.usecases.category_usecases import CategoryUsecase
from src.infra.db.repositories.category_repository_interface import CategoryRepository
from src.usecases.order_usecases import OrderUsecase
from src.usecases.order_item_usecases import OrderItemUsecase
from src.infra.db.repositories.order_repository_interface import OrderRepository
from src.infra.db.repositories.order_item_repository_interface import OrderItemRepository



def get_db():
    with DBConnectionHandler() as db:
        yield db


def get_user_usecase(db=Depends(get_db)):
    user_repository = UserRepository(db)
    account_repository = AccountRepository(db)
    return UserUsecase(user_repository, account_repository)


def get_account_usecase(db=Depends(get_db)):
    account_repository = AccountRepository(db)
    return CreateAccountUsecase(account_repository)


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
