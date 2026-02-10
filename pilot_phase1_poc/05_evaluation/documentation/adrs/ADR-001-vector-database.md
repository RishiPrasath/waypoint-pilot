# ADR-001: Vector Database Selection -- ChromaDB

**Status**: Accepted
**Date**: 2025-01-20

## Context

The Waypoint co-pilot POC requires a vector database for storing and retrieving document embeddings. The system must support:

- Local-first operation with no cloud dependency
- Persistent storage across application restarts
- Metadata filtering alongside vector similarity search
- Zero API cost during development and evaluation
- Compatibility with Python ingestion pipeline and Node.js backend (via subprocess bridge)

The POC budget constrains total LLM API costs to under $10, making cloud-hosted vector databases impractical.

## Decision

Use **ChromaDB 0.5.23** with `PersistentClient` for local file-system storage.

Configuration:
- Collection name: `waypoint_kb`
- Embedding model: ChromaDB default (`all-MiniLM-L6-v2` via ONNX runtime)
- Embedding dimensions: 384
- Persistence path: `chroma_db/` within each workspace directory

The Node.js backend communicates with ChromaDB through a Python bridge script (`query_chroma.py`) that reads JSON from stdin and outputs JSON to stdout.

## Alternatives Considered

| Alternative | Reason for Rejection |
|------------|---------------------|
| **Pinecone** | Cloud-hosted, requires API key, incurs per-query costs. Exceeds POC budget model and adds cloud dependency. |
| **Weaviate** | Heavier runtime footprint (Docker container or standalone binary). Over-engineered for a 30-doc KB. |
| **pgvector** | Requires a running PostgreSQL instance. Adds infrastructure complexity for a single-developer POC. |
| **FAISS** | No built-in metadata filtering. Would require a separate metadata store alongside the vector index, increasing complexity. |

## Consequences

**Positive**:
- Zero cost -- runs entirely offline with no API keys required
- Built-in ONNX embedding model eliminates separate model hosting
- PersistentClient provides durable storage without external database process
- Metadata filtering (category, doc_id, source_type) works natively in queries
- Simple Python API for both ingestion and retrieval

**Negative**:
- Single-node only -- no horizontal scaling for production workloads
- No built-in replication or backup mechanism
- Python-only client requires subprocess bridge from Node.js (adds ~200ms per query)
- Limited query analytics and monitoring compared to managed solutions
- Collection size limited by local disk and memory
