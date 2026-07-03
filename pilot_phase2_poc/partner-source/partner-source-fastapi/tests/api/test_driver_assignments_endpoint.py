from fastapi.testclient import TestClient

from app.main import app


def test_list_driver_assignments_returns_two_active_items() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20")

    assert response.status_code == 200
    body = response.json()
    assert body["driverId"] == "DRV-2001"
    assert body["totalItems"] == 2
    assert [item["orderId"] for item in body["items"]] == ["ORD-1001", "ORD-1002"]


def test_driver_with_no_assignments_returns_empty_items() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-2003/assignments?page=1&pageSize=20")

    assert response.status_code == 200
    assert response.json()["items"] == []


def test_missing_driver_assignments_returns_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-9999/assignments?page=1&pageSize=20")

    assert response.status_code == 404
    assert response.json()["errorCode"] == "DRIVER_NOT_FOUND"
