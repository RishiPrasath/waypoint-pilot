from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "rag-service"
    environment: str = "local"
    groq_api_key: SecretStr | None = None
    qdrant_api_key: SecretStr | None = None
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "rag_chunks"
    qdrant_vector_size: int = 384
    qdrant_distance: str = "Cosine"
    qdrant_payload_schema_version: str = "v1"
    qdrant_embedding_model_name: str | None = None
    qdrant_embedding_model_version: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="RAG_", env_file=".env", extra="ignore"
    )

    def require_groq_api_key(self) -> str:
        if self.groq_api_key is None:
            raise RuntimeError("RAG_GROQ_API_KEY is required for Groq-backed features")

        return self.groq_api_key.get_secret_value()

    def require_qdrant_api_key(self) -> str:
        if self.qdrant_api_key is None:
            raise RuntimeError(
                "RAG_QDRANT_API_KEY is required for Qdrant-backed features"
            )

        return self.qdrant_api_key.get_secret_value()
