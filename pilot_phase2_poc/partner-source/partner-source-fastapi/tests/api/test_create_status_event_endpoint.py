from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app


def test_create_status_event_returns_201_and_mutates_order_status(driver_2001_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        headers=driver_2001_headers,
        json={
            "driverId": "DRV-2001",
            "status": "DELIVERED",
            "occurredAt": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
        },
    )

    assert response.status_code == 201
    assert response.json()["previousStatus"] == "OUT_FOR_DELIVERY"
    assert response.json()["orderCurrentStatus"] == "DELIVERED"

    status_response = client.get("/api/v1/orders/ORD-1001/status", headers=driver_2001_headers)
    assert status_response.json()["currentStatus"] == "DELIVERED"


def test_unassigned_driver_returns_403_problem_detail(driver_2002_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        headers=driver_2002_headers,
        json={"driverId": "DRV-2002", "status": "DELIVERED"},
    )

    assert response.status_code == 403
    assert response.json()["errorCode"] == "ORDER_NOT_ASSIGNED_TO_DRIVER"


def test_malformed_status_event_body_returns_invalid_request(driver_2001_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        headers=driver_2001_headers,
        json={"driverId": "DRV-2001"},
    )

    assert response.status_code == 400
    assert response.json()["errorCode"] == "INVALID_REQUEST"
