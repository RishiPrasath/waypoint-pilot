from app.core.config import Settings


def test_settings_have_safe_local_defaults():
    settings = Settings()

    assert settings.environment == "local"
    assert settings.service_name == "rag-service"
