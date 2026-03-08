from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

from ..config.config_env import EnvironmentVariables

# PostgreSQL
database_url = EnvironmentVariables.DATABASE_URL


engine = create_engine(database_url)


@asynccontextmanager  # Corregir error de lifespan en main.py
async def create_db_and_tables(app: FastAPI):
    # from .models import expense_model, user_model - También se pueden realizar aquí las importaciones para la creación, dejando las relaciones entre tablas con comillas ("user" y "Expense")

    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
