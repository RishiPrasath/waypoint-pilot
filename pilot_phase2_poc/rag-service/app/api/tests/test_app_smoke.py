from app.main import app


def test_fastapi_app_exists():
    assert app.title == "rag-service"
