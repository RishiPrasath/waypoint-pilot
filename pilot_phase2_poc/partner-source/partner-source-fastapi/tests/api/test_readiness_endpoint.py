from fastapi.testclient import TestClient

from app.main import app


def test_ready_returns_ready_response() -> None:
    client = TestClient(app)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "READY",
        "service": "partner-source",
        "checks": {
            "persistence": "UP",
            "seedData": "UP",
        },
    }
