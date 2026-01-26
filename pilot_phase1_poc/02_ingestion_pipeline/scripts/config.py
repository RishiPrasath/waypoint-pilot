"""
Waypoint Ingestion Pipeline Configuration

Centralized configuration module that loads settings from .env
and provides typed constants for the ingestion pipeline.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Path Resolution
# -----------------------------------------------------------------------------

# Get the pipeline root directory (02_ingestion_pipeline/)
PIPELINE_ROOT = Path(__file__).parent.parent.resolve()

# Load .env from the pipeline root
load_dotenv(PIPELINE_ROOT / ".env")

# -----------------------------------------------------------------------------
# Path Configuration
# -----------------------------------------------------------------------------

# ChromaDB storage directory
CHROMA_PERSIST_PATH: Path = PIPELINE_ROOT / os.getenv(
    "CHROMA_PERSIST_PATH", "./chroma_db"
)

# Knowledge base documents directory (kb/ contains only content documents)
KNOWLEDGE_BASE_PATH: Path = (
    PIPELINE_ROOT / os.getenv("KNOWLEDGE_BASE_PATH", "../01_knowledge_base/kb")
).resolve()

# Logs directory
LOG_DIR: Path = PIPELINE_ROOT / "logs"

# -----------------------------------------------------------------------------
# Embedding Configuration
# -----------------------------------------------------------------------------

# ChromaDB default embeddings (all-MiniLM-L6-v2 via ONNX)
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "default")
EMBEDDING_DIMENSIONS: int = int(os.getenv("EMBEDDING_DIMENSIONS", "384"))

# -----------------------------------------------------------------------------
# Chunking Configuration
# -----------------------------------------------------------------------------

# Chunk size in characters (~150 tokens)
CHUNK_SIZE: int = 600

# Chunk overlap in characters (15%)
CHUNK_OVERLAP: int = 90

# Text splitter separators (in order of priority)
SEPARATORS: list[str] = ["\n## ", "\n### ", "\n\n", "\n"]

# -----------------------------------------------------------------------------
# ChromaDB Configuration
# -----------------------------------------------------------------------------

# Collection name for the knowledge base
COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "waypoint_kb")

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# -----------------------------------------------------------------------------
# Directory Auto-Creation
# -----------------------------------------------------------------------------

# Create directories if they don't exist
CHROMA_PERSIST_PATH.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Verify knowledge base exists (don't create - it should already exist)
if not KNOWLEDGE_BASE_PATH.exists():
    raise FileNotFoundError(
        f"Knowledge base directory not found: {KNOWLEDGE_BASE_PATH}"
    )
