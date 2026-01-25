# Task 1.6: (Optional) Local Virtual Environment Setup

## Persona

> You are a Python developer with expertise in virtual environment management and dependency isolation.
> You ensure reproducible local development environments that mirror containerized production setups.

---

## Context

### Project Background
The local virtual environment is the primary execution method for the Waypoint ingestion pipeline. This provides fast iteration during development, debugging, and testing with minimal dependencies (no PyTorch or CUDA required).

### Current State
- Environment setup complete (Tasks 1.1-1.3)
- `requirements.txt` configured with ChromaDB (uses built-in default embeddings)
- `.env` configured (no API key needed)
- No local virtual environment exists yet

### Reference Documents
- Pipeline Plan: `docs/00_ingestion_pipeline_plan.md`
- Implementation Roadmap: `docs/01_implementation_roadmap.md`
- Environment Files: `.env`, `.env.example`

### Dependencies
- Task 1.1 (Folder Structure) - ✅ Complete
- Task 1.2 (requirements.txt) - ✅ Complete
- Task 1.3 (Environment Files) - ✅ Complete

---

## Task

### Objective
Create and configure a local Python virtual environment that can run the ingestion pipeline using ChromaDB's built-in default embeddings (lightweight ONNX runtime).

### Requirements
1. Create a Python 3.11+ virtual environment in `venv/` directory
2. Install all dependencies from `requirements.txt`
3. Verify all required packages import correctly
4. Verify environment variables load from `.env`
5. Test local embedding generation

### Specifications

**Virtual Environment Setup**:
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Required Package Imports**:
| Package | Import Statement |
|---------|------------------|
| chromadb | `import chromadb` |
| chromadb (embeddings) | `from chromadb.utils import embedding_functions` |
| frontmatter | `import frontmatter` |
| langchain | `from langchain_text_splitters import RecursiveCharacterTextSplitter` |
| dotenv | `from dotenv import load_dotenv` |
| tqdm | `from tqdm import tqdm` |

**Environment Variable Verification**:
```python
from dotenv import load_dotenv
import os

load_dotenv()

# Required variables
assert os.getenv('EMBEDDING_MODEL') == 'default', "EMBEDDING_MODEL mismatch"
assert os.getenv('EMBEDDING_DIMENSIONS') == '384', "EMBEDDING_DIMENSIONS mismatch"
assert os.getenv('COLLECTION_NAME') == 'waypoint_kb', "COLLECTION_NAME mismatch"
print("All environment variables OK")
```

**ChromaDB Default Embeddings Test**:
```python
from chromadb.utils import embedding_functions

ef = embedding_functions.DefaultEmbeddingFunction()
result = ef(['test embedding'])
assert len(result[0]) == 384, "Unexpected embedding dimensions"
print(f"ChromaDB default OK - {len(result[0])} dimensions")
```

### Constraints
- Virtual environment must be in `venv/` directory (already in `.gitignore`)
- Must use Python 3.11 or higher
- Must work on Windows (primary development platform)
- Must not modify any existing files
- No API key required (local embeddings)

### Acceptance Criteria
- [ ] `venv/` directory created
- [ ] All packages from `requirements.txt` installed
- [ ] `import chromadb` works
- [ ] `from chromadb.utils import embedding_functions` works
- [ ] `import frontmatter` works
- [ ] `from langchain_text_splitters import RecursiveCharacterTextSplitter` works
- [ ] `from dotenv import load_dotenv` works
- [ ] Environment variables load correctly from `.env`
- [ ] ChromaDB default embeddings return 384-dimension vectors

---

## Format

### Output Structure
```
02_ingestion_pipeline/
├── venv/                    # Created (gitignored)
│   ├── Scripts/             # Windows executables
│   ├── Lib/                 # Installed packages
│   └── pyvenv.cfg           # Virtual env config
└── (existing files unchanged)
```

### Documentation
No new files required. Virtual environment is for local development only.

### Validation Commands

**Windows PowerShell**:
```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase1_poc\02_ingestion_pipeline

# Create and activate venv
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Test imports
python -c "import chromadb; print('chromadb OK')"
python -c "from chromadb.utils import embedding_functions; print('embedding_functions OK')"
python -c "import frontmatter; print('frontmatter OK')"
python -c "from langchain_text_splitters import RecursiveCharacterTextSplitter; print('langchain OK')"
python -c "from dotenv import load_dotenv; print('dotenv OK')"

# Test environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'EMBEDDING_MODEL: {os.getenv(\"EMBEDDING_MODEL\")}')"

# Test ChromaDB default embeddings
python -c "from chromadb.utils import embedding_functions; ef = embedding_functions.DefaultEmbeddingFunction(); result = ef(['test']); print(f'OK - {len(result[0])} dimensions')"
```

### Expected Output
```
chromadb OK
embedding_functions OK
frontmatter OK
langchain OK
dotenv OK
EMBEDDING_MODEL: default
OK - 384 dimensions
```

---

## Notes

The local virtual environment is the primary execution method. It is useful for:
- Fast iteration during development
- IDE integration (autocomplete, linting)
- Running individual tests
- Minimal dependencies (no PyTorch, no CUDA)

ChromaDB's built-in default embedding function uses the same model (all-MiniLM-L6-v2) but via lightweight ONNX runtime instead of PyTorch.
