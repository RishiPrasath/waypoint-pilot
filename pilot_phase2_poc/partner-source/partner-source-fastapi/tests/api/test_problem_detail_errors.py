from fastapi.testclient import TestClient

from app.main import app


def assert_problem_detail(body: dict, error_code: str, status: int) -> None:
    assert body["type"]
    assert body["title"]
    assert body["status"] == status
    assert body["detail"]
    assert body["instance"]
    assert body["errorCode"] == error_code
    assert body["correlationId"]


def test_missing_order_uses_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-9999/status")

    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
    assert_problem_detail(response.json(), "ORDER_NOT_FOUND", 404)


def test_invalid_order_id_uses_invalid_request_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/INVALID/status")

    assert response.status_code == 400
    assert_problem_detail(response.json(), "INVALID_REQUEST", 400)


def test_deprecated_transition_code_is_not_returned() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-9999/status")

    assert "ORDER_TRANSITION_INVALID" not in response.text
