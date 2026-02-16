import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    API_TITLE: str = os.getenv("API_TITLE", "OrderFlow API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")

settings = Settings()
