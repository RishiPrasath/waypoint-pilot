from fastapi.testclient import TestClient

from app.main import app


def test_get_order_timeline_returns_contract_shape() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20")

    assert response.status_code == 200
    body = response.json()
    assert body["orderId"] == "ORD-1001"
    assert body["page"] == 1
    assert body["pageSize"] == 20
    assert body["totalItems"] == 5
    assert [item["eventId"] for item in body["items"]] == [
        "EVT-4001",
        "EVT-4002",
        "EVT-4003",
        "EVT-4004",
        "EVT-4005",
    ]


def test_invalid_order_timeline_id_returns_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/INVALID/timeline")

    assert response.status_code == 400
    assert response.json()["errorCode"] == "INVALID_REQUEST"
