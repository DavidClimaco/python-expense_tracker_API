from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import col, select

from ..models.user_model import User
from .config_env import EnvironmentVariables
from .db import SessionDep

password_hash = PasswordHash.recommended()

# Esquema para validar una ruta que contenga el token autenticado en el header Authorization = Bearer <Token>
# oauth2_scheme = APIKeyHeader(name="Authorization")
oauth2_scheme = OAuth2PasswordBearer("/login")


def get_password_hash(password: str):
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, EnvironmentVariables.SECRET_KEY, EnvironmentVariables.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token,
            EnvironmentVariables.SECRET_KEY,
            algorithms=[EnvironmentVariables.ALGORITHM],
        )
        body = payload.get("sub")
        if body is None:
            raise credentials_exception
        token_data = User(email=body)
    except InvalidTokenError:
        raise credentials_exception

    statement = select(User).where(col(User.email).match(token_data.email))
    user_db = session.exec(statement=statement).first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.commit()
    session.refresh(user_db)
    return user_db
