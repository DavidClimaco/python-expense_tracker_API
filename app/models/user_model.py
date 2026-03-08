from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

# from app.models.expense_model import Expense - No lo importamos aquí porque crea una importación circular, se agrega entre comillas "Expense" para que espere a cargar todos los datos

# Para corregir errores de typing en el linter
if TYPE_CHECKING:
    from ..models.expense_model import Expense


class UserAccountBase(SQLModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)


class UserBase(UserAccountBase):
    name: str = Field(default=None)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    expenses: list["Expense"] = Relationship(
        back_populates="user",
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


# Account base
class UserLogin(UserAccountBase):
    pass
