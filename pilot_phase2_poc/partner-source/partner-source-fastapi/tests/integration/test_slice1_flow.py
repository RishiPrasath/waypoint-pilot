from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app


def test_slice1_happy_path_status_event_flow() -> None:
    client = TestClient(app)

    assert client.get("/health").json()["status"] == "UP"
    assert client.get("/ready").json()["status"] == "READY"

    before = client.get("/api/v1/orders/ORD-1001/status")
    assert before.status_code == 200
    assert before.json()["currentStatus"] == "OUT_FOR_DELIVERY"

    timeline_before = client.get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20")
    assert timeline_before.status_code == 200
    assert timeline_before.json()["totalItems"] == 5

    assert client.get("/api/v1/drivers/DRV-2001").json()["activeAssignmentCount"] == 2
    assert client.get("/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20").json()["totalItems"] == 2

    created = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={
            "driverId": "DRV-2001",
            "status": "DELIVERED",
            "occurredAt": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
        },
    )
    assert created.status_code == 201
    assert created.json()["previousStatus"] == "OUT_FOR_DELIVERY"
    assert created.json()["newStatus"] == "DELIVERED"
    assert created.json()["orderCurrentStatus"] == "DELIVERED"

    after = client.get("/api/v1/orders/ORD-1001/status")
    assert after.json()["currentStatus"] == "DELIVERED"

    timeline_after = client.get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20")
    assert timeline_after.json()["totalItems"] == 6
    assert timeline_after.json()["items"][-1]["status"] == "DELIVERED"


def test_slice1_negative_paths_match_contract_error_codes() -> None:
    client = TestClient(app)

    unassigned = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={"driverId": "DRV-2002", "status": "DELIVERED"},
    )
    assert unassigned.status_code == 403
    assert unassigned.json()["errorCode"] == "ORDER_NOT_ASSIGNED_TO_DRIVER"

    missing_driver = client.post(
        "/api/v1/orders/ORD-1001/status-events",
        json={"driverId": "DRV-9999", "status": "DELIVERED"},
    )
    assert missing_driver.status_code == 404
    assert missing_driver.json()["errorCode"] == "DRIVER_NOT_FOUND"

    invalid_transition = client.post(
        "/api/v1/orders/ORD-1003/status-events",
        json={"driverId": "DRV-2001", "status": "OUT_FOR_DELIVERY"},
    )
    assert invalid_transition.status_code == 409
    assert invalid_transition.json()["errorCode"] == "INVALID_STATUS_TRANSITION"
