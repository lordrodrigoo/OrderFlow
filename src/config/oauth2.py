import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
API_V1_AUTH = os.getenv("API_V1_AUTH")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=API_V1_AUTH)
