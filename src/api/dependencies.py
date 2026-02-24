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
from src.infra.db.repositories.category_repository_interface import CategoryRepositoryInterface as CategoryRepository


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
