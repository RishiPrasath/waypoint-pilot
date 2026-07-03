from fastapi.testclient import TestClient

from app.main import app


def test_get_driver_profile_returns_contract_shape() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-2001")

    assert response.status_code == 200
    body = response.json()
    assert body["driverId"] == "DRV-2001"
    assert body["displayName"] == "A. Kumar"
    assert body["availabilityStatus"] == "AVAILABLE"
    assert body["activeAssignmentCount"] == 2


def test_missing_driver_returns_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-9999")

    assert response.status_code == 404
    assert response.json()["errorCode"] == "DRIVER_NOT_FOUND"
