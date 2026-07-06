from fastapi.testclient import TestClient

from app.main import app


def test_demo_driver_login_returns_token_and_principal() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/auth/demo-login", json={"actorType": "DRIVER", "actorId": "DRV-2001"})

    assert response.status_code == 200
    body = response.json()
    assert body["accessToken"] == "demo-driver-2001-token"
    assert body["tokenType"] == "Bearer"
    assert body["principal"]["role"] == "DELIVERY_DRIVER"
    assert body["principal"]["actorId"] == "DRV-2001"


def test_demo_csa_login_returns_token_and_principal() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/auth/demo-login", json={"actorType": "USER", "actorId": "CSA-5001"})

    assert response.status_code == 200
    body = response.json()
    assert body["accessToken"] == "demo-csa-5001-token"
    assert body["principal"]["role"] == "CUSTOMER_SERVICE_AGENT"


def test_unknown_demo_driver_login_returns_driver_not_found() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/auth/demo-login", json={"actorType": "DRIVER", "actorId": "DRV-9999"})

    assert response.status_code == 404
    assert response.json()["errorCode"] == "DRIVER_NOT_FOUND"


def test_unsupported_demo_login_identity_returns_invalid_request() -> None:
    client = TestClient(app)

    response = client.post("/api/v1/auth/demo-login", json={"actorType": "USER", "actorId": "CSA-9999"})

    assert response.status_code == 400
    assert response.json()["errorCode"] == "INVALID_REQUEST"
