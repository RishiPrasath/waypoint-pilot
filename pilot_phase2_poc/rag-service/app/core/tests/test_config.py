from app.core.config import Settings


def test_settings_have_safe_local_defaults():
    settings = Settings()

    assert settings.environment == "local"
    assert settings.service_name == "rag-service"


def test_secret_backed_features_fail_only_when_used():
    settings = Settings()

    try:
        settings.require_groq_api_key()
    except RuntimeError as exc:
        assert "RAG_GROQ_API_KEY" in str(exc)
    else:
        raise AssertionError("expected missing Groq key to fail when used")


def test_secret_values_are_hidden_in_repr():
    settings = Settings(groq_api_key="super-secret")

    assert "super-secret" not in repr(settings)
