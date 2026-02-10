"""
Waypoint Retrieval Optimization Pipeline Configuration

Forked from 02_ingestion_pipeline/scripts/config.py (Week 1).
Key changes:
  - CHUNK_SIZE and CHUNK_OVERLAP are parameterized via .env
  - KNOWLEDGE_BASE_PATH defaults to local ./kb
  - CHROMA_PERSIST_PATH defaults to local ./chroma_db
  - Empty KB directory warns instead of raising FileNotFoundError
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Path Resolution
# -----------------------------------------------------------------------------

# Get the pipeline root directory (04_retrieval_optimization/)
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

# Knowledge base documents directory (local kb/)
KNOWLEDGE_BASE_PATH: Path = (
    PIPELINE_ROOT / os.getenv("KNOWLEDGE_BASE_PATH", "./kb")
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
# Chunking Configuration (parameterized via .env)
# -----------------------------------------------------------------------------

# Chunk size in characters (~150 tokens at 600)
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "600"))

# Chunk overlap in characters (15% at 90/600)
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "90"))

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

# Warn if knowledge base directory is empty (don't raise - content added later)
if not KNOWLEDGE_BASE_PATH.exists():
    logger.warning(
        f"Knowledge base directory not found: {KNOWLEDGE_BASE_PATH}. "
        f"Creating empty directory."
    )
    KNOWLEDGE_BASE_PATH.mkdir(parents=True, exist_ok=True)
elif not any(KNOWLEDGE_BASE_PATH.iterdir()):
    logger.warning(
        f"Knowledge base directory is empty: {KNOWLEDGE_BASE_PATH}. "
        f"Documents will be added during Task 6."
    )

# Log loaded configuration at DEBUG level
logger.debug(f"PIPELINE_ROOT: {PIPELINE_ROOT}")
logger.debug(f"KNOWLEDGE_BASE_PATH: {KNOWLEDGE_BASE_PATH}")
logger.debug(f"CHROMA_PERSIST_PATH: {CHROMA_PERSIST_PATH}")
logger.debug(f"CHUNK_SIZE: {CHUNK_SIZE}")
logger.debug(f"CHUNK_OVERLAP: {CHUNK_OVERLAP}")
logger.debug(f"COLLECTION_NAME: {COLLECTION_NAME}")
