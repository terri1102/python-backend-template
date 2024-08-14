from typing import Generator
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, None, None]:
    client = TestClient(app)
    yield client
