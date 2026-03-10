from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from ..config.db import SessionDep
from ..config.security import get_current_user
from ..models.expense_model import Expense, ExpenseCreate, ExpenseUpdate
from ..models.user_model import User

router = APIRouter()


@router.get("/expenses", status_code=status.HTTP_200_OK, tags=["Expenses"])
async def list_expenses(
    session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]
):
    """Regresa una lista con todos los Expenses del usuario"""
    statement = select(Expense).where(Expense.user_id == current_user.id)
    return session.exec(statement).all()


@router.get("/expenses/{expense_id}", status_code=status.HTTP_200_OK, tags=["Expenses"])
async def get_expense(
    session: SessionDep,
    expense_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Regresa un Expense del usuario según su identificador"""
    expense_db = session.get(Expense, expense_id)
    if not expense_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    if expense_db.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You do not have access to this resource",
        )
    return expense_db


@router.post("/expenses", status_code=status.HTTP_201_CREATED, tags=["Expenses"])
async def add_expense(
    session: SessionDep,
    expense_data: ExpenseCreate,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Permite agregar un Expense a la base de datos vinculado al usuario logueado"""
    try:
        new_expense = Expense.model_validate(
            expense_data, update={"user_id": current_user.id}
        )
        session.add(new_expense)
        session.commit()
        session.refresh(new_expense)
        return new_expense
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The ammount and category fields are required",
        )


@router.patch(
    "/expenses/{expense_id}", status_code=status.HTTP_200_OK, tags=["Expenses"]
)
async def update_expense(
    session: SessionDep,
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Actualización de los datos de un Expense del usuario"""
    expense_db = session.get(Expense, expense_id)
    if not expense_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    if expense_db.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have access to this resource",
        )

    expense_dict = expense_data.model_dump(exclude_unset=True)
    expense_db.sqlmodel_update(expense_dict, update={"updated_at": datetime.now()})
    session.add(expense_db)
    session.commit()
    session.refresh(expense_db)
    return expense_db


@router.delete(
    "/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Expenses"]
)
async def delete_expense(
    session: SessionDep,
    expense_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Eliminación de un Expense que pertenezca al usuario"""
    expense_db = session.get(Expense, expense_id)
    if not expense_db:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Expense not found")
    if expense_db.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have access to this resource",
        )
    session.delete(expense_db)
    session.commit()
