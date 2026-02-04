#pylint: disable=redefined-outer-name
#pylint: disable=unused-import
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.infra.db.settings.base import Base

# ENTITIES IMPORT FIX
from src.infra.db.entities.user import UserEntity
from src.infra.db.entities.account import AccountEntity
from src.infra.db.entities.address import AddressEntity
from src.infra.db.entities.category import CategoryEntity
from src.infra.db.entities.product import ProductEntity
from src.infra.db.entities.order import OrderEntity
from src.infra.db.entities.order_item import OrderItemEntity
from src.infra.db.entities.review import ReviewEntity

load_dotenv()

class DBConnectionHandler:

    def __init__(self) -> None:
        self.__connection_string = os.getenv("DB_URL")
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def get_session(self):
        session_make = sessionmaker(bind=self.__engine)
        return session_make()

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

engine = DBConnectionHandler().get_engine()
Base.metadata.create_all(bind=engine)
