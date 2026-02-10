# ADR-005: Embedding Model Selection -- all-MiniLM-L6-v2 via ONNX

**Status**: Accepted
**Date**: 2025-01-20

## Context

The Waypoint co-pilot requires an embedding model to convert document chunks and user queries into vector representations for similarity search. Requirements:

- Must work entirely offline (no API calls per embedding operation)
- Must run on a development machine without a dedicated GPU
- Must be compatible with ChromaDB's embedding and query pipeline
- Embedding quality must be sufficient for freight forwarding domain terminology
- Fast enough for real-time query embedding (< 1 second)

## Decision

Use **all-MiniLM-L6-v2** via the ONNX runtime, which is ChromaDB's built-in default embedding model.

Configuration:
- Model: `all-MiniLM-L6-v2` (Sentence Transformers)
- Runtime: ONNX (via `onnxruntime` Python package)
- Dimensions: 384
- Max sequence length: 256 tokens
- Configuration in code: `EMBEDDING_MODEL = "default"` (ChromaDB auto-selects)

No explicit model download or configuration is required -- ChromaDB handles model loading automatically on first use.

## Alternatives Considered

| Alternative | Reason for Rejection |
|------------|---------------------|
| **OpenAI text-embedding-ada-002** | Requires API calls per embedding operation. Adds per-query cost and cloud dependency. Violates the offline-first requirement. |
| **Sentence-Transformers with PyTorch** | Requires PyTorch installation (1.5-2GB). Significantly heavier dependency than ONNX runtime. Needs CUDA for reasonable inference speed. |
| **Cohere embed-english-v3** | Cloud-hosted API. Adds cost and network dependency. No free tier sufficient for 700+ chunk ingestion plus queries. |
| **OpenAI text-embedding-3-small** | Same cloud/cost issues as ada-002. Better quality but still requires API calls. |
| **BGE-small-en-v1.5** | Comparable quality to MiniLM but not ChromaDB's default. Would require explicit model configuration and separate download. |

## Consequences

**Positive**:
- Zero API cost -- all embeddings generated locally
- Fully offline operation -- no network required after initial model download
- Lightweight ONNX runtime (~50MB) vs. PyTorch (~1.5GB)
- No GPU required -- runs on CPU with acceptable performance
- Zero configuration -- ChromaDB uses this model by default
- Consistent embeddings between ingestion and query time (same model guaranteed)

**Negative**:
- 384 dimensions is smaller than state-of-the-art models (OpenAI ada-002: 1536-d, text-embedding-3-large: 3072-d). Lower dimensionality may miss nuanced semantic distinctions.
- English-focused model. May underperform on Malay, Bahasa Indonesia, or Thai terms that appear in ASEAN regulatory content.
- Max sequence length of 256 tokens means chunks exceeding this limit are truncated during embedding, potentially losing information.
- May miss domain-specific semantics for freight forwarding jargon not well-represented in the model's training data (MiniLM trained on general English text).
- No fine-tuning capability in the ONNX variant -- model is used as-is.
