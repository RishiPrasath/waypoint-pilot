from fastapi.testclient import TestClient

from app.main import app


def test_missing_token_returns_unauthenticated() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-1001/status")

    assert response.status_code == 401
    assert response.json()["errorCode"] == "UNAUTHENTICATED"


def test_invalid_token_returns_unauthenticated() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-1001/status", headers={"Authorization": "Bearer invalid-token"})

    assert response.status_code == 401
    assert response.json()["errorCode"] == "UNAUTHENTICATED"


def test_driver_cannot_read_unassigned_order(driver_2002_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-1001/status", headers=driver_2002_headers)

    assert response.status_code == 403
    assert response.json()["errorCode"] == "ACCESS_DENIED"


def test_csa_can_read_order_but_cannot_write_status_event(csa_headers: dict[str, str]) -> None:
    client = TestClient(app)

    read_response = client.get("/api/v1/orders/ORD-1001/status", headers=csa_headers)
    assert read_response.status_code == 200

    write_response = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        headers=csa_headers,
        json={"driverId": "DRV-2001", "status": "DELIVERED"},
    )

    assert write_response.status_code == 403
    assert write_response.json()["errorCode"] == "ACCESS_DENIED"


def test_spoofed_driver_id_returns_access_denied(driver_2001_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        headers=driver_2001_headers,
        json={"driverId": "DRV-2002", "status": "DELIVERED"},
    )

    assert response.status_code == 403
    assert response.json()["errorCode"] == "ACCESS_DENIED"
