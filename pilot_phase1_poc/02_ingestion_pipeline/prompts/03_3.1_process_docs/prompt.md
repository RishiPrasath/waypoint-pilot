# Task 3.1: Create Document Processor Module

## Persona

> You are a Python developer specializing in document processing pipelines.
> You follow PEP-8 style guidelines and write clean, well-documented code.
> You prioritize robust error handling and graceful degradation for edge cases.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot for freight forwarding. The ingestion pipeline processes 29 markdown documents from the knowledge base, extracts metadata from YAML frontmatter, and prepares them for chunking and embedding.

### Current State
- ✅ Environment setup complete (venv, requirements.txt)
- ✅ Configuration module exists at `scripts/config.py`
- 📁 Knowledge base at `01_knowledge_base/kb/` has 29 documents across 4 categories:
  - `kb/01_regulatory/` (14 docs) - Singapore Customs, ASEAN trade
  - `kb/02_carriers/` (6 docs) - Ocean & Air carriers
  - `kb/03_reference/` (3 docs) - Incoterms, HS codes
  - `kb/04_internal_synthetic/` (6 docs) - Policies, procedures

**Note**: The `kb/` folder contains ONLY content documents (no meta files).

### Reference Documents
- Roadmap: `docs/01_implementation_roadmap.md`
- Config: `scripts/config.py`
- Sample doc: `../01_knowledge_base/kb/01_regulatory/singapore_customs/sg_import_procedures.md`

### Dependencies
- Task 2.1 (config.py) ✅ Complete
- `python-frontmatter` package installed
- `KNOWLEDGE_BASE_PATH` available from config

---

## Task

### Objective
Create `scripts/process_docs.py` that discovers all markdown documents in the knowledge base, parses their YAML frontmatter, and returns structured document objects ready for chunking.

### Requirements

1. **`discover_documents(path: Path) -> list[Path]`**
   - Recursively find all `.md` files under the given path
   - The `kb/` folder contains only content documents (no exclusions needed)
   - Return sorted list of Path objects

2. **`parse_frontmatter(content: str) -> dict`**
   - Parse YAML frontmatter from document content
   - Return empty dict if no frontmatter found
   - Use `python-frontmatter` library

3. **`extract_content(content: str) -> str`**
   - Extract markdown content after frontmatter
   - Strip leading/trailing whitespace

4. **`get_category_from_path(file_path: Path) -> str`**
   - Extract category from path (e.g., `01_regulatory`, `02_carriers`)
   - Return the top-level category folder name

5. **`generate_doc_id(file_path: Path) -> str`**
   - Generate unique doc ID from file path
   - Format: `{category}_{filename}` (without .md extension)
   - Example: `01_regulatory_sg_import_procedures`

6. **`parse_document(file_path: Path) -> dict`**
   - Main function that combines all above
   - Returns structured document object

### Document Object Schema

```python
{
    "doc_id": str,           # Unique identifier
    "file_path": str,        # Absolute path as string
    "title": str,            # From frontmatter or filename
    "source_org": str,       # source_organization field
    "source_urls": list,     # List of URL strings (extract url field from nested objects)
    "source_type": str,      # public_regulatory | public_carrier | synthetic_internal
    "last_updated": str,     # YYYY-MM-DD format
    "jurisdiction": str,     # SG, MY, ID, TH, VN, PH, ASEAN, Global
    "category": str,         # From path: regulatory, carriers, reference, internal_synthetic
    "use_cases": list,       # List of use case IDs [UC-1.1, UC-2.3]
    "content": str,          # Full markdown content (without frontmatter)
    "char_count": int,       # Length of content
}
```

### Frontmatter Field Mapping

The knowledge base uses these frontmatter field names:

| Frontmatter Field | Document Object Field |
|-------------------|----------------------|
| `title` | `title` |
| `source_organization` | `source_org` |
| `source_urls` | `source_urls` (extract `url` from nested objects) |
| `source_type` | `source_type` |
| `last_updated` | `last_updated` |
| `jurisdiction` | `jurisdiction` |
| `category` | (use path-based category instead) |
| `use_cases` | `use_cases` |

### Sample Frontmatter Structure

```yaml
---
title: Singapore Import Procedures
source_organization: Singapore Customs
source_urls:
  - url: https://www.customs.gov.sg/businesses/importing-goods/overview/
    description: Overview of Singapore import procedures
    retrieved_date: 2025-01-22
source_type: public_regulatory
last_updated: 2025-01-22
jurisdiction: SG
category: customs
use_cases: [UC-1.1, UC-2.1]
---
```

### Constraints
- Handle missing optional fields gracefully (use sensible defaults)
- Log warnings for documents with parsing issues but don't fail
- Don't modify the original markdown files
- Keep memory efficient (don't load all docs at once unless needed)

### Acceptance Criteria
- [ ] File created at `scripts/process_docs.py`
- [ ] `discover_documents()` finds all 29 content documents
- [ ] `parse_frontmatter()` correctly parses YAML
- [ ] `extract_content()` returns clean markdown
- [ ] `get_category_from_path()` extracts correct category
- [ ] `generate_doc_id()` creates unique IDs
- [ ] `parse_document()` returns complete document object
- [ ] Handles missing optional fields without crashing

---

## Format

### Output Structure
```
scripts/
└── process_docs.py
```

### Code Style
- Python 3.11+ type hints
- Docstrings for all public functions
- Logging using Python's `logging` module
- Import from `scripts.config` for paths

### Module Structure
```python
"""
Document processor for Waypoint knowledge base.

The knowledge base is located in 01_knowledge_base/kb/ which contains
only content documents (no meta files).
"""

import logging
from pathlib import Path

import frontmatter

from scripts.config import KNOWLEDGE_BASE_PATH

logger = logging.getLogger(__name__)


def discover_documents(path: Path) -> list[Path]:
    ...

def parse_frontmatter(content: str) -> dict:
    ...

def extract_content(content: str) -> str:
    ...

def get_category_from_path(file_path: Path) -> str:
    ...

def generate_doc_id(file_path: Path) -> str:
    ...

def parse_document(file_path: Path) -> dict:
    ...

# Convenience function
def load_all_documents() -> list[dict]:
    """Load and parse all documents from the knowledge base."""
    ...
```

### Validation Commands
```bash
# Test discovery
python -c "from scripts.process_docs import discover_documents; from scripts.config import KNOWLEDGE_BASE_PATH; docs = discover_documents(KNOWLEDGE_BASE_PATH); print(f'Found {len(docs)} documents')"

# Test single document parse
python -c "from scripts.process_docs import parse_document; from scripts.config import KNOWLEDGE_BASE_PATH; doc = parse_document(KNOWLEDGE_BASE_PATH / '01_regulatory/singapore_customs/sg_import_procedures.md'); print(doc['title'], doc['source_org'])"

# Test load all
python -c "from scripts.process_docs import load_all_documents; docs = load_all_documents(); print(f'Loaded {len(docs)} docs, total chars: {sum(d[\"char_count\"] for d in docs)}')"
```

---

## Execution Checklist

After implementing, verify:
1. [ ] Discovers exactly 29 documents from `kb/` folder
2. [ ] Parses frontmatter from all 4 categories correctly
3. [ ] Extracts clean content without YAML block
4. [ ] Generates unique doc_ids
5. [ ] Handles documents with missing optional fields
6. [ ] All validation commands pass
