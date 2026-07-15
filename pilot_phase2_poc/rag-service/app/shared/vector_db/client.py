from typing import Literal

from pydantic import BaseModel


class VectorDbConfig(BaseModel):
    collection_name: str
    vector_size: int
    distance: Literal["Cosine", "Dot", "Euclid"] = "Cosine"
    payload_schema_version: str = "v1"
    embedding_model_name: str | None = None
    embedding_model_version: str | None = None
