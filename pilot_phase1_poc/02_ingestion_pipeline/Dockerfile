# Waypoint Ingestion Pipeline Dockerfile
# Single-stage build - Gemini API (no local model caching needed)

FROM python:3.11-slim

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY scripts/ ./scripts/

# Create directories for volumes
RUN mkdir -p /app/knowledge_base /app/chroma_db /app/logs

# Default environment variables (overridden by docker-compose)
ENV KNOWLEDGE_BASE_PATH=/app/knowledge_base \
    CHROMA_PERSIST_PATH=/app/chroma_db \
    LOG_DIR=/app/logs \
    COLLECTION_NAME=waypoint_kb \
    EMBEDDING_MODEL=gemini-embedding-001 \
    EMBEDDING_DIMENSIONS=768 \
    LOG_LEVEL=INFO

# Entrypoint
ENTRYPOINT ["python", "scripts/ingest.py"]
