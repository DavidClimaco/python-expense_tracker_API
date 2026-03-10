import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from app.config.security import get_current_user

from ..config.db import get_session
from ..main import app
from ..models.user_model import User

sqlite_name = "db-test.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"


engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    mock_user = User(
        email="example@example.com", password="password", name="Example", id=1
    )

    def get_session_override():
        return session

    def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
