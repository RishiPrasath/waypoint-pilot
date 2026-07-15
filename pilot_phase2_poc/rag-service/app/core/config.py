from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "rag-service"
    environment: str = "local"

    model_config = SettingsConfigDict(env_prefix="RAG_", env_file=".env")
