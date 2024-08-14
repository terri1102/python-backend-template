from fastapi.testclient import TestClient


def test_health_check(test_client: TestClient) -> None:
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_health_check_content_type(test_client: TestClient) -> None:
    response = test_client.get("/health")
    assert response.headers["content-type"] == "application/json"
