from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from ..config.db import SessionDep
from ..config.security import get_password_hash
from ..models.user_model import User, UserCreate, UserUpdate

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def register_user(
    session: SessionDep,
    user_data: UserCreate,
):
    """Permite registrar un nuevo usuario en la base de datos"""
    try:
        new_user = User.model_validate(user_data.model_dump())
        new_user.sqlmodel_update(
            new_user, update={"password": get_password_hash(user_data.password)}
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email, password and name fields are required",
        )


@router.patch("/register/{user_id}", status_code=status.HTTP_200_OK, tags=["Users"])
async def update_user(session: SessionDep, user_id: int, user_data: UserUpdate):
    """Actualizar la información de un usuario en la base de datos"""
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    data_dict = user_data.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(data_dict, update={"updated_at": datetime.now()})
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.delete(
    "/register/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"]
)
async def delete_user(session: SessionDep, user_id):
    """Elimina un usuario de la base de datos"""
    delete_post = session.get(User, user_id)

    if not delete_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    session.delete(delete_post)
    session.commit()
