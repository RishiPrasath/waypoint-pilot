from types import SimpleNamespace

from app.core.config import Settings
from app.shared.vector_db.client import (
    QdrantVectorDbClient,
    VectorDbConfig,
    VectorPoint,
)


class MockQdrantClient:
    def __init__(self):
        self.calls = []

    def upsert(self, *, collection_name, points):
        self.calls.append(("upsert", collection_name, points))
        return {"status": "ok"}

    def search(self, *, collection_name, query_vector, limit, query_filter=None):
        self.calls.append(
            ("search", collection_name, query_vector, limit, query_filter)
        )
        return [
            SimpleNamespace(
                id="chunk-1",
                score=0.92,
                payload={"payload_schema_version": "v1"},
            )
        ]

    def delete(self, *, collection_name, points_selector):
        self.calls.append(("delete", collection_name, points_selector))
        return {"status": "deleted"}


def test_vector_db_config_has_collection_contract_fields():
    config = VectorDbConfig(
        collection_name="rag_chunks_test",
        vector_size=384,
        distance="Cosine",
        payload_schema_version="v1",
        embedding_model_name="test-embedding-model",
        embedding_model_version="2026-07-15",
    )

    assert config.collection_name == "rag_chunks_test"
    assert config.vector_size == 384
    assert config.distance == "Cosine"
    assert config.payload_schema_version == "v1"
    assert config.embedding_model_name == "test-embedding-model"
    assert config.embedding_model_version == "2026-07-15"


def test_vector_db_config_loads_collection_settings():
    settings = Settings(
        qdrant_collection_name="rag_chunks_local",
        qdrant_vector_size=768,
        qdrant_distance="Dot",
        qdrant_payload_schema_version="v2",
        qdrant_embedding_model_name="local-embedding-model",
    )

    config = VectorDbConfig.from_settings(settings)

    assert config.collection_name == "rag_chunks_local"
    assert config.vector_size == 768
    assert config.distance == "Dot"
    assert config.payload_schema_version == "v2"
    assert config.embedding_model_name == "local-embedding-model"


def test_qdrant_boundary_supports_upsert_search_and_delete_cleanup():
    mock_client = MockQdrantClient()
    config = VectorDbConfig(collection_name="rag_chunks_test", vector_size=3)
    client = QdrantVectorDbClient(config=config, client=mock_client)

    upsert_result = client.upsert(
        [
            VectorPoint(
                id="chunk-1",
                vector=[0.1, 0.2, 0.3],
                payload={"payload_schema_version": "v1"},
            )
        ]
    )
    search_results = client.search([0.1, 0.2, 0.3], limit=1)
    delete_result = client.delete_points(["chunk-1"])

    assert upsert_result == {"status": "ok"}
    assert search_results[0].id == "chunk-1"
    assert search_results[0].score == 0.92
    assert delete_result == {"status": "deleted"}
    assert mock_client.calls == [
        (
            "upsert",
            "rag_chunks_test",
            [
                {
                    "id": "chunk-1",
                    "vector": [0.1, 0.2, 0.3],
                    "payload": {"payload_schema_version": "v1"},
                }
            ],
        ),
        ("search", "rag_chunks_test", [0.1, 0.2, 0.3], 1, None),
        ("delete", "rag_chunks_test", {"points": ["chunk-1"]}),
    ]
