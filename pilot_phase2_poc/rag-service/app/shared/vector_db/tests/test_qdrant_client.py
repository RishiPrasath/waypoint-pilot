from app.shared.vector_db.client import VectorDbConfig


def test_vector_db_config_has_collection_name():
    config = VectorDbConfig(
        collection_name="rag_chunks_test",
        vector_size=384,
        distance="Cosine",
        payload_schema_version="v1",
        embedding_model_name="test-embedding-model",
    )

    assert config.collection_name == "rag_chunks_test"
    assert config.vector_size == 384
    assert config.distance == "Cosine"
    assert config.payload_schema_version == "v1"
