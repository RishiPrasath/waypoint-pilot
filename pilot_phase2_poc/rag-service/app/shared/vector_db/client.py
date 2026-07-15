from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

from app.core.config import Settings


DistanceMetric = Literal["Cosine", "Dot", "Euclid"]


class VectorDbConfig(BaseModel):
    collection_name: str
    vector_size: int = Field(gt=0)
    distance: DistanceMetric = "Cosine"
    payload_schema_version: str = "v1"
    embedding_model_name: str | None = None
    embedding_model_version: str | None = None

    @classmethod
    def from_settings(cls, settings: Settings) -> "VectorDbConfig":
        return cls(
            collection_name=settings.qdrant_collection_name,
            vector_size=settings.qdrant_vector_size,
            distance=settings.qdrant_distance,
            payload_schema_version=settings.qdrant_payload_schema_version,
            embedding_model_name=settings.qdrant_embedding_model_name,
            embedding_model_version=settings.qdrant_embedding_model_version,
        )


class VectorPoint(BaseModel):
    id: str | int
    vector: list[float]
    payload: dict[str, Any] = Field(default_factory=dict)


class VectorSearchMatch(BaseModel):
    id: str | int
    score: float
    payload: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="ignore")


class QdrantClientBoundary(Protocol):
    def upsert(self, *, collection_name: str, points: list[dict[str, Any]]) -> Any:
        ...

    def search(
        self,
        *,
        collection_name: str,
        query_vector: list[float],
        limit: int,
        query_filter: dict[str, Any] | None = None,
    ) -> list[Any]:
        ...

    def delete(
        self,
        *,
        collection_name: str,
        points_selector: dict[str, Any],
    ) -> Any:
        ...


class QdrantVectorDbClient:
    def __init__(self, config: VectorDbConfig, client: QdrantClientBoundary):
        self.config = config
        self._client = client

    def upsert(self, points: list[VectorPoint]) -> Any:
        return self._client.upsert(
            collection_name=self.config.collection_name,
            points=[point.model_dump() for point in points],
        )

    def search(
        self,
        vector: list[float],
        *,
        limit: int = 10,
        query_filter: dict[str, Any] | None = None,
    ) -> list[VectorSearchMatch]:
        results = self._client.search(
            collection_name=self.config.collection_name,
            query_vector=vector,
            limit=limit,
            query_filter=query_filter,
        )

        return [self._coerce_search_match(result) for result in results]

    def delete_points(self, point_ids: list[str | int]) -> Any:
        return self._client.delete(
            collection_name=self.config.collection_name,
            points_selector={"points": point_ids},
        )

    @staticmethod
    def _coerce_search_match(result: Any) -> VectorSearchMatch:
        if isinstance(result, dict):
            return VectorSearchMatch.model_validate(result)

        return VectorSearchMatch(
            id=result.id,
            score=result.score,
            payload=getattr(result, "payload", {}) or {},
        )
