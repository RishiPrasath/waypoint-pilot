from fastapi.testclient import TestClient

from app.main import app


def test_get_driver_profile_returns_contract_shape(driver_2001_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-2001", headers=driver_2001_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["driverId"] == "DRV-2001"
    assert body["displayName"] == "A. Kumar"
    assert body["availabilityStatus"] == "AVAILABLE"
    assert body["activeAssignmentCount"] == 2


def test_driver_cannot_read_another_driver_profile(driver_2001_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-2002", headers=driver_2001_headers)

    assert response.status_code == 403
    assert response.json()["errorCode"] == "ACCESS_DENIED"
