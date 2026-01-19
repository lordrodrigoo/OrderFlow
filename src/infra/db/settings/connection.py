import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

class DBConnectionHandler:

    def __init__(self) -> None:
        self.__connection_string = "{db_url}://{user}:{password}@{host}:{port}/{db_name}".format(
            db_url = os.getenv("DB_URL"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT"),
            db_name = os.getenv("DB_NAME"),
        )
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
