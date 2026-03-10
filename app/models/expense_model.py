from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

# from .user_model import (
#     User,  # Clase hija si debe de tener el import para poder validar la relación, aun así se puede utilizar comillas ("User") para evitar problemas
# )

if TYPE_CHECKING:
    from ..models.user_model import User


class CategoryEnum(str, Enum):
    GROCERIES = "groceries"
    LEISURE = "leisure"
    ELECTRONICS = "electronics"
    UTILITIES = "utilites"
    CLOTHING = "clothing"
    HEALTH = "health"
    OTHERS = "others"


class ExpenseBase(SQLModel):
    description: str | None = Field(default=None)
    ammount: float = Field(default=None)
    category: CategoryEnum = Field(default=None)


class Expense(ExpenseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="expenses")
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass
