from fastapi.testclient import TestClient

from app.main import app


def test_get_order_status_returns_contract_shape(driver_2001_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-1001/status", headers=driver_2001_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["orderId"] == "ORD-1001"
    assert body["currentStatus"] == "OUT_FOR_DELIVERY"
    assert body["statusLabel"] == "Out for delivery"
    assert body["deliveryWindow"] is not None
    assert body["assignedDriver"]["driverId"] == "DRV-2001"


def test_get_missing_order_returns_404(csa_headers: dict[str, str]) -> None:
    client = TestClient(app)

    response = client.get("/api/v1/orders/ORD-9999/status", headers=csa_headers)

    assert response.status_code == 404
