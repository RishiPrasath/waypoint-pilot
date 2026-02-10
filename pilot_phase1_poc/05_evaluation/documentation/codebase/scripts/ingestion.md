# Ingestion Pipeline

Layer 3 documentation for `config.py`, `process_docs.py`, `chunker.py`, and `ingest.py`.

These four modules form the complete ingestion pipeline: configuration, document discovery and parsing, semantic chunking, and ChromaDB storage.

---

## config.py

Central configuration module. All other scripts import constants from here.

### Path Resolution

```python
PIPELINE_ROOT = Path(__file__).parent.parent.resolve()
```

`PIPELINE_ROOT` resolves to the workspace root (e.g., `05_evaluation/`). A `.env` file at this location is loaded via `python-dotenv`.

### Exported Constants

| Constant | Type | Default | Source | Description |
|----------|------|---------|--------|-------------|
| `PIPELINE_ROOT` | `Path` | (computed) | `__file__` | Workspace root directory |
| `CHROMA_PERSIST_PATH` | `Path` | `./chroma_db` | `.env` or default | ChromaDB storage directory |
| `KNOWLEDGE_BASE_PATH` | `Path` | `./kb` | `.env` or default | Knowledge base documents root |
| `LOG_DIR` | `Path` | `./logs` | hardcoded | Log file output directory |
| `EMBEDDING_MODEL` | `str` | `"default"` | `.env` or default | ChromaDB embedding model (all-MiniLM-L6-v2 ONNX) |
| `EMBEDDING_DIMENSIONS` | `int` | `384` | `.env` or default | Embedding vector dimensions |
| `CHUNK_SIZE` | `int` | `600` | `.env` or default | Chunk size in characters (~150 tokens) |
| `CHUNK_OVERLAP` | `int` | `90` | `.env` or default | Overlap between chunks (15% of 600) |
| `SEPARATORS` | `list[str]` | `["\n## ", "\n### ", "\n\n", "\n"]` | hardcoded | Text splitter separator priority |
| `COLLECTION_NAME` | `str` | `"waypoint_kb"` | `.env` or default | ChromaDB collection name |
| `LOG_LEVEL` | `str` | `"INFO"` | `.env` or default | Logging level |

### Auto-Creation Behavior

On import, `config.py` automatically:
1. Creates `CHROMA_PERSIST_PATH` if it does not exist
2. Creates `LOG_DIR` if it does not exist
3. Creates `KNOWLEDGE_BASE_PATH` with a warning if it does not exist
4. Warns if `KNOWLEDGE_BASE_PATH` exists but is empty

### Environment Variable Override

All parameterized values can be overridden via `.env`:

```env
CHROMA_PERSIST_PATH=./chroma_db
KNOWLEDGE_BASE_PATH=./kb
EMBEDDING_MODEL=default
EMBEDDING_DIMENSIONS=384
CHUNK_SIZE=600
CHUNK_OVERLAP=90
COLLECTION_NAME=waypoint_kb
LOG_LEVEL=INFO
```

---

## process_docs.py

Document processor. Discovers markdown files, parses YAML frontmatter, and returns structured document dictionaries.

### Functions

#### `discover_documents(path: Path) -> list[Path]`

Recursively discovers all `.md` files under the given path, excluding files in `pdfs/` subdirectories.

**Parameters:**
- `path` (`Path`): Root path to search (typically `KNOWLEDGE_BASE_PATH`, i.e., `kb/`)

**Returns:** Sorted list of `Path` objects for each discovered document.

**Exclusion logic:** Any file whose relative path (from `path`) contains a `pdfs` part is excluded. This prevents PDF extract files from being ingested -- their content has been selectively merged into main docs.

```python
documents = [
    f for f in path.rglob("*.md")
    if "pdfs" not in f.relative_to(path).parts
]
```

**Example:**
```python
from scripts.process_docs import discover_documents
from scripts.config import KNOWLEDGE_BASE_PATH

paths = discover_documents(KNOWLEDGE_BASE_PATH)
# Returns ~30 Path objects like:
#   kb/01_regulatory/sg_import_procedures.md
#   kb/02_carriers/maersk_ocean.md
#   ...
# Excludes:
#   kb/01_regulatory/pdfs/some_extract.md
```

---

#### `parse_frontmatter(content: str) -> dict`

Extracts YAML frontmatter from raw markdown content.

**Parameters:**
- `content` (`str`): Raw markdown content including `---` delimited frontmatter

**Returns:** Dictionary of frontmatter fields. Returns empty dict if parsing fails.

**Example:**
```python
content = "---\ntitle: Test Doc\njurisdiction: SG\n---\n\nBody text."
meta = parse_frontmatter(content)
# {'title': 'Test Doc', 'jurisdiction': 'SG'}
```

---

#### `extract_content(content: str) -> str`

Extracts body text after frontmatter. This is the text that gets embedded -- frontmatter is stripped.

**Parameters:**
- `content` (`str`): Raw markdown content with potential frontmatter

**Returns:** Clean markdown body content (stripped), without frontmatter delimiters or YAML fields.

**Example:**
```python
content = "---\ntitle: Test\n---\n\nBody text here."
body = extract_content(content)
# "Body text here."
```

---

#### `get_category_from_path(file_path: Path) -> str`

Extracts category folder name from the document's file path relative to `KNOWLEDGE_BASE_PATH`.

**Parameters:**
- `file_path` (`Path`): Absolute path to the document

**Returns:** First directory component of the relative path (e.g., `"01_regulatory"`). Returns `"unknown"` if category cannot be determined.

---

#### `generate_doc_id(file_path: Path) -> str`

Generates a unique document ID from the file path.

**Parameters:**
- `file_path` (`Path`): Absolute path to the document

**Returns:** String in format `{category}_{filename_stem}`, e.g., `"01_regulatory_sg_import_procedures"`.

---

#### `_extract_source_urls(source_urls_field) -> list[str]`

Internal helper. Extracts URL strings from the `source_urls` frontmatter field, handling both simple string lists and nested object structures (`{url: "...", description: "..."}`).

**Parameters:**
- `source_urls_field`: The `source_urls` value from frontmatter (list of strings or dicts)

**Returns:** Flat list of URL strings.

---

#### `parse_document(file_path: Path) -> dict`

Parses a single markdown document into a structured dictionary.

**Parameters:**
- `file_path` (`Path`): Absolute path to the markdown document

**Returns:** Dictionary with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `doc_id` | `str` | Unique ID: `{category}_{filename}` |
| `file_path` | `str` | Absolute file path (resolved) |
| `title` | `str` | From frontmatter `title`, fallback to filename |
| `source_org` | `str` | From frontmatter `source_organization` |
| `source_urls` | `list[str]` | Extracted URLs |
| `source_type` | `str` | `public_regulatory`, `public_carrier`, or `synthetic_internal` |
| `last_updated` | `str` | ISO date string |
| `jurisdiction` | `str` | Country/region code (SG, MY, ASEAN, etc.) |
| `category` | `str` | Category folder name |
| `use_cases` | `list[str]` | Use case IDs (UC-1.1, etc.) |
| `retrieval_keywords` | `list[str]` | Keywords for retrieval optimization |
| `content` | `str` | Body text only (no frontmatter) |
| `char_count` | `int` | Length of `content` |

**Raises:** Re-raises file read exceptions.

**Example:**
```python
from pathlib import Path
from scripts.process_docs import parse_document

doc = parse_document(Path("kb/01_regulatory/sg_import_procedures.md"))
print(doc["doc_id"])       # "01_regulatory_sg_import_procedures"
print(doc["title"])        # "Singapore Import Procedures"
print(doc["char_count"])   # 4523
print(doc["content"][:50]) # "## Overview\n\nSingapore Customs regulates..."
```

---

#### `load_all_documents() -> list[dict]`

Discovers and parses all documents from `KNOWLEDGE_BASE_PATH`.

**Parameters:** None (uses `KNOWLEDGE_BASE_PATH` from config).

**Returns:** List of parsed document dictionaries. Failed documents are logged and skipped.

**Example:**
```python
from scripts.process_docs import load_all_documents

docs = load_all_documents()
print(f"Loaded {len(docs)} documents")           # "Loaded 30 documents"
print(f"Total chars: {sum(d['char_count'] for d in docs)}")
```

---

## chunker.py

Semantic chunking engine. Splits documents into chunks while preserving metadata and section context.

Uses `RecursiveCharacterTextSplitter` from `langchain-text-splitters`.

### Functions

#### `generate_chunk_id(doc_id: str, index: int) -> str`

Generates a unique chunk ID with zero-padded index.

**Parameters:**
- `doc_id` (`str`): The document ID
- `index` (`int`): The chunk index (0-based)

**Returns:** Chunk ID in format `{doc_id}_chunk_{index:03d}`.

**Example:**
```python
generate_chunk_id("01_regulatory_sg_import", 5)
# "01_regulatory_sg_import_chunk_005"
```

---

#### `extract_section_header(content: str, position: int) -> str`

Finds the most recent `##` section header before a given character position. Does not match `###` headers.

**Parameters:**
- `content` (`str`): Full document content
- `position` (`int`): Character position in content

**Returns:** Header text (without `##` prefix), or empty string if none found.

**Regex pattern:** `(?:^|\n)## ([^\n]+)`

---

#### `extract_subsection_header(content: str, position: int) -> str`

Finds the most recent `###` subsection header before a given character position.

**Parameters:**
- `content` (`str`): Full document content
- `position` (`int`): Character position in content

**Returns:** Subsection header text (without `###` prefix), or empty string if none found.

**Regex pattern:** `(?:^|\n)### ([^\n]+)`

---

#### `_find_chunk_position(content: str, chunk_text: str, start_from: int = 0) -> int`

Internal helper. Locates a chunk's position within the original document content. Uses the first 100 characters of the chunk for matching to handle overlap.

**Parameters:**
- `content` (`str`): Full document content
- `chunk_text` (`str`): The chunk text to locate
- `start_from` (`int`): Position to start searching from (default 0)

**Returns:** Character position, or `start_from` if not found.

---

#### `chunk_document(doc: dict) -> list[dict]`

Splits a single document into chunks while preserving all metadata.

**Parameters:**
- `doc` (`dict`): Parsed document dict from `process_docs.parse_document()`

**Returns:** List of chunk dictionaries with the following fields:

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `chunk_id` | `str` | Generated | `{doc_id}_chunk_{NNN}` |
| `chunk_index` | `int` | Generated | 0-based chunk position |
| `chunk_text` | `str` | Splitter output | The chunk content |
| `chunk_char_count` | `int` | Computed | Length of `chunk_text` |
| `section_header` | `str` | Extracted | Nearest `##` header |
| `subsection_header` | `str` | Extracted | Nearest `###` header |
| `doc_id` | `str` | Inherited | From parent document |
| `file_path` | `str` | Inherited | From parent document |
| `title` | `str` | Inherited | From parent document |
| `source_org` | `str` | Inherited | From parent document |
| `source_urls` | `list[str]` | Inherited | From parent document |
| `source_type` | `str` | Inherited | From parent document |
| `last_updated` | `str` | Inherited | From parent document |
| `jurisdiction` | `str` | Inherited | From parent document |
| `category` | `str` | Inherited | From parent document |
| `use_cases` | `list[str]` | Inherited | From parent document |
| `retrieval_keywords` | `list[str]` | Inherited | From parent document |
| `content` | `str` | Inherited | Full document body (for reference) |
| `char_count` | `int` | Inherited | Full document char count |

**Splitter configuration:**
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,         # from config.CHUNK_SIZE
    chunk_overlap=90,       # from config.CHUNK_OVERLAP
    separators=["\n## ", "\n### ", "\n\n", "\n"],  # from config.SEPARATORS
    length_function=len,
)
```

**Example:**
```python
from scripts.process_docs import parse_document
from scripts.chunker import chunk_document
from pathlib import Path

doc = parse_document(Path("kb/01_regulatory/sg_import_procedures.md"))
chunks = chunk_document(doc)

print(f"Document: {doc['title']}")
print(f"Chunks: {len(chunks)}")
print(f"First chunk ID: {chunks[0]['chunk_id']}")
print(f"First chunk section: {chunks[0]['section_header']}")
```

---

#### `chunk_all_documents(docs: list[dict]) -> list[dict]`

Chunks all documents and returns a flat list of all chunks.

**Parameters:**
- `docs` (`list[dict]`): List of parsed document dicts from `load_all_documents()`

**Returns:** Flat list of all chunk dicts across all documents. Failed documents are logged and skipped.

**Example:**
```python
from scripts.process_docs import load_all_documents
from scripts.chunker import chunk_all_documents

docs = load_all_documents()
chunks = chunk_all_documents(docs)
print(f"Total chunks: {len(chunks)}")  # ~709
```

---

## ingest.py

Main entry point for the ingestion pipeline. Orchestrates discover, parse, chunk, embed, and store.

### CLI Arguments

```
usage: ingest.py [-h] [-v] [-d] [--category CATEGORY] [--clear]

optional arguments:
  -v, --verbose         Show detailed chunk information
  -d, --dry-run         Process documents without storing to ChromaDB
  --category CATEGORY   Only process specific category (e.g., 01_regulatory)
  --clear               Clear existing collection before ingesting
```

### Functions

#### `parse_args(args: Optional[list] = None) -> argparse.Namespace`

Parses command-line arguments.

**Parameters:**
- `args` (`Optional[list]`): Argument list for testing. Uses `sys.argv` if None.

**Returns:** `argparse.Namespace` with `verbose`, `dry_run`, `category`, `clear` attributes.

---

#### `initialize_chromadb() -> tuple`

Initializes ChromaDB persistent client and collection.

**Parameters:** None.

**Returns:** Tuple of `(client, collection)`. Uses `CHROMA_PERSIST_PATH` and `COLLECTION_NAME` from config. The collection is created with `get_or_create_collection` using `DefaultEmbeddingFunction()`.

---

#### `ingest_document(doc: dict, collection, dry_run: bool = False, verbose: bool = False) -> int`

Ingests a single document into ChromaDB.

**Parameters:**
- `doc` (`dict`): Parsed document dict from `parse_document()`
- `collection`: ChromaDB collection object
- `dry_run` (`bool`): If True, processes but does not store (default False)
- `verbose` (`bool`): If True, logs chunk details (default False)

**Returns:** Number of chunks processed.

**ChromaDB metadata stored per chunk:**

| Field | Value |
|-------|-------|
| `doc_id` | Document ID |
| `title` | Document title |
| `source_org` | Source organization |
| `source_type` | Document type |
| `jurisdiction` | Country/region code |
| `category` | Category folder |
| `section_header` | Nearest `##` header |
| `subsection_header` | Nearest `###` header |
| `chunk_index` | Chunk position (int) |
| `file_path` | Absolute file path |
| `source_urls` | Comma-joined URL string |
| `retrieval_keywords` | Comma-joined keyword string |
| `use_cases` | Comma-joined use case string |

Note: List fields (`source_urls`, `retrieval_keywords`, `use_cases`) are comma-joined into strings because ChromaDB metadata only supports scalar types.

---

#### `run_ingestion(args: argparse.Namespace) -> dict`

Runs the full ingestion pipeline.

**Parameters:**
- `args` (`argparse.Namespace`): Parsed CLI arguments

**Returns:** Summary dictionary:

```python
{
    "documents_processed": int,
    "documents_failed": int,
    "chunks_processed": int,
    "stored": int,
    "elapsed_time": float,
    "failed_docs": list[str],
}
```

**Pipeline steps:**
1. Initialize ChromaDB client and collection
2. If `--clear`, delete all existing chunks from collection
3. Discover documents via `discover_documents()`
4. Filter by `--category` if specified
5. For each document: parse, chunk, ingest
6. Return summary statistics

---

#### `print_summary(results: dict, args: argparse.Namespace)`

Prints human-readable ingestion summary to stdout.

---

#### `main()`

CLI entry point. Parses args, configures logging, runs ingestion, prints summary. Exits with code 1 if any documents failed.

### Usage Examples

```bash
# Full ingestion
python scripts/ingest.py

# Clear existing data and re-ingest
python scripts/ingest.py --clear

# Dry run with verbose output
python scripts/ingest.py --dry-run --verbose

# Ingest only regulatory documents
python scripts/ingest.py --category 01_regulatory

# Clear and re-ingest with verbose logging
python scripts/ingest.py --clear --verbose
```

### Expected Output

```
==================================================
Waypoint Ingestion Pipeline
==================================================

Configuration:
  Knowledge Base: C:\...\05_evaluation\kb
  ChromaDB Path:  C:\...\05_evaluation\chroma_db
  Collection:     waypoint_kb
  Chunk Size:     600
  Chunk Overlap:  90
  Dry Run:        No
  Clear:          Yes

Processing documents...
  [1/30] 01_regulatory_sg_import_procedures: 24 chunks [stored]
  [2/30] 01_regulatory_sg_export_procedures: 18 chunks [stored]
  ...

==================================================
Summary
==================================================
  Documents processed: 30
  Documents failed:    0
  Chunks processed:    709
  Stored:              709
  Time elapsed:        3.42s

Done! Collection 'waypoint_kb' now contains 709 chunks.
```
