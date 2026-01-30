# Task 1.2: Fix source_urls in Ingestion

## Persona

> You are a Python developer with expertise in data pipelines and vector databases.
> You follow clean code practices and ensure metadata integrity for RAG systems.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The ingestion pipeline stores document chunks in ChromaDB with metadata for citation. Currently, `source_urls` from document frontmatter is NOT being stored in ChromaDB metadata, which will break citation URLs in responses.

### Current State
- Task 1.1 complete: KB and ingestion copied to `03_rag_pipeline/`
- `ingest.py` stores 10 metadata fields but omits `source_urls`
- `source_urls` exists in document frontmatter and passes through `chunker.py`
- ChromaDB collection exists but lacks `source_urls` field

### Reference Documents
- `03_rag_pipeline/ingestion/scripts/ingest.py` - Line 136-150, metadata dict
- `03_rag_pipeline/ingestion/scripts/chunker.py` - Already includes source_urls in chunk dict
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - Citation format requirements

### Dependencies
- Task 1.1: Copy KB and Ingestion ✅

---

## Task

### Objective
Add `source_urls` to ChromaDB metadata so citations can include clickable source URLs.

### Requirements

1. **Update ingest.py metadata**
   - Add `source_urls` field to the metadata dict in `ingest_document()` function
   - Convert list to comma-separated string: `",".join(chunk["source_urls"])`
   - Handle empty source_urls gracefully (empty string if none)

2. **Re-run ingestion with --clear**
   - Clear existing collection and re-ingest all 29 documents
   - Verify 483 chunks are stored

3. **Verify source_urls in metadata**
   - Query ChromaDB to confirm source_urls field exists
   - Check a few documents have correct URLs

### Specifications

**Current metadata dict** (line 136-150 in ingest.py):
```python
metadatas = [
    {
        "doc_id": chunk["doc_id"],
        "title": chunk["title"],
        "source_org": chunk["source_org"],
        "source_type": chunk["source_type"],
        "jurisdiction": chunk["jurisdiction"],
        "category": chunk["category"],
        "section_header": chunk["section_header"],
        "subsection_header": chunk["subsection_header"],
        "chunk_index": chunk["chunk_index"],
        "file_path": chunk["file_path"],
        # MISSING: source_urls
    }
    for chunk in chunks
]
```

**Required change** - Add after `file_path`:
```python
"source_urls": ",".join(chunk.get("source_urls", [])),
```

### Constraints
- Do NOT modify chunker.py (already passes source_urls correctly)
- Do NOT modify other metadata fields
- source_urls must be a string (ChromaDB doesn't support list values in metadata)

### Acceptance Criteria
- [ ] `ingest.py` updated to include `source_urls` in metadata dict
- [ ] Re-ingestion complete with `--clear` flag (483 chunks)
- [ ] Query confirms `source_urls` field exists in metadata
- [ ] At least one regulatory doc has correct Singapore Customs URL
- [ ] Internal/synthetic docs have empty string for source_urls

### TDD Requirements
- N/A (simple field addition, existing tests cover ingestion flow)

---

## Format

### Output Structure
Single file modified: `ingestion/scripts/ingest.py`

### Code Style
```python
# Add this line after file_path in the metadata dict:
"source_urls": ",".join(chunk.get("source_urls", [])),
```

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline/ingestion

# Activate venv
venv\Scripts\activate

# Re-ingest with clear
python -m scripts.ingest --clear

# Verify source_urls in metadata (should show 'source_urls' in keys)
python -c "
import chromadb
client = chromadb.PersistentClient('./chroma_db')
col = client.get_collection('waypoint_kb')
result = col.get(limit=1)
print('Metadata keys:', list(result['metadatas'][0].keys()))
print('source_urls value:', result['metadatas'][0].get('source_urls', 'MISSING'))
"

# Check a regulatory document has URL
python -c "
import chromadb
client = chromadb.PersistentClient('./chroma_db')
col = client.get_collection('waypoint_kb')
result = col.get(where={'category': 'customs'}, limit=1)
print('Category:', result['metadatas'][0]['category'])
print('source_urls:', result['metadatas'][0].get('source_urls', 'MISSING'))
"

# Verify total count is 483
python -c "
import chromadb
client = chromadb.PersistentClient('./chroma_db')
col = client.get_collection('waypoint_kb')
print(f'Total chunks: {col.count()}')
"
```

### Expected Output
```
Metadata keys: ['doc_id', 'title', 'source_org', 'source_type', 'jurisdiction', 'category', 'section_header', 'subsection_header', 'chunk_index', 'file_path', 'source_urls']
source_urls value: https://www.customs.gov.sg/...

Total chunks: 483
```
