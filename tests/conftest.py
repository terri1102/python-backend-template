from typing import Generator
import pytest
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.engine import Engine
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from app.main import app
from app.api.dependencies import get_db


@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, None, None]:
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer("postgres:13") as postgres:
        postgres.start()
        yield postgres


@pytest.fixture(scope="module")
def db_engine(postgres_container: PostgresContainer) -> Generator[Engine, None, None]:
    engine = create_engine(postgres_container.get_connection_url())
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    with Session(db_engine) as session:
        yield session


@pytest.fixture(autouse=True)
def override_get_db(db_session: Session) -> Generator[None, None, None]:
    def _get_db_override() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides[get_db] = get_db
