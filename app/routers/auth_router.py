from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import col, select

from ..config.db import SessionDep
from ..config.security import create_access_token, verify_password
from ..models.user_model import User, UserLogin

router = APIRouter()


# @router.post("/login", status_code=status.HTTP_200_OK, tags=["Auth"])
# async def login(
#     session: SessionDep,
#     user_data: Annotated[UserLogin, Depends(OAuth2PasswordRequestForm)],
# ):
#     """Valida y permite el inicio de sesión según el email y password ingresado por el usuario, además genera un token JWT"""
#     statement = select(User).where(col(User.email).match(user_data.email))
#     user_db = session.exec(statement).first()
#     if not user_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     auth_user = verify_password(user_data.password, user_db.password)
#     if not auth_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Password incorrect, try again",
#         )
#     # time_token_expires = timedelta(minutes=15)
#     token = create_access_token({"body": user_db.email})
#     return token


@router.post("/login", status_code=status.HTTP_200_OK, tags=["Auth"])
async def login(
    session: SessionDep,
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Valida y permite el inicio de sesión según el email y password ingresado por el usuario, además genera un token JWT"""
    # OAuth2 solo permite username y password para la verificación, así que para la consulta usamos el email que viene en el username del login
    user_email = user_data.username
    user_password = user_data.password
    # statement = select(User).where(col(User.email).match(user_email)) <- Mejor forma para validar en PostgreSQL, pero en testing para SQLite falla
    statement = select(User).where(User.email == user_email)
    user_db = session.exec(statement).first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    auth_user = verify_password(user_password, user_db.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password incorrect, try again",
        )
    time_token_expires = timedelta(minutes=30)
    token = create_access_token(
        {"sub": user_db.email}, expires_delta=time_token_expires
    )
    return {
        "access_token": token,
        "token_type": "bearer",
    }  # Al usar OAuth2PasswordRequest Form se requiere que se devuelva el token en formato JSOn así como se ve en el return


@router.post("/logout", status_code=status.HTTP_200_OK, tags=["Auth"])
async def logout(session: SessionDep):
    """Permite cerrar sesión al usuario"""
    pass
