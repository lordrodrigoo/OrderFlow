import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from pwdlib import PasswordHash
from jose import jwt, ExpiredSignatureError, JWTError
from src.dto.response.token_response import TokenPayload
from src.exceptions.exception_handlers_auth import (
    TokenExpiredException,
    TokenInvalidException,
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except ExpiredSignatureError as exc:
        raise TokenExpiredException() from exc
    except JWTError as exc:
        raise TokenInvalidException() from exc
