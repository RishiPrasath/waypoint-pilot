# Vector DB Boundary

`QdrantVectorDbClient` wraps Qdrant-style upsert, search, and delete calls
behind `app.shared.vector_db`. Unit tests use an injected mock client so Stage 1
CI does not require a running Qdrant service.

Optional local smoke test:

```powershell
docker run --rm -p 6333:6333 qdrant/qdrant
```

Use `Settings` with `RAG_QDRANT_*` environment variables to point the wrapper at
the local service once the real SDK client is wired in a later task.
