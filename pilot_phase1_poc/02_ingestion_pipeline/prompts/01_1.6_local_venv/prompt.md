# Task 1.6: (Optional) Local Virtual Environment Setup

## Persona

> You are a Python developer with expertise in virtual environment management and dependency isolation.
> You ensure reproducible local development environments that mirror containerized production setups.

---

## Context

### Project Background
While Docker is the primary execution method for the Waypoint ingestion pipeline, a local virtual environment provides a fallback for development, debugging, and testing without Docker overhead. This is especially useful for rapid iteration during script development.

### Current State
- Docker setup complete (Tasks 1.1-1.5)
- `requirements.txt` updated for Google Gemini API embeddings
- `.env` configured with GOOGLE_API_KEY
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
Create and configure a local Python virtual environment that can run the ingestion pipeline without Docker, using the same dependencies and configuration as the containerized version.

### Requirements
1. Create a Python 3.11+ virtual environment in `venv/` directory
2. Install all dependencies from `requirements.txt`
3. Verify all required packages import correctly
4. Verify environment variables load from `.env`
5. Test Gemini API connectivity

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
| google-genai | `from google import genai` |
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
assert os.getenv('GOOGLE_API_KEY'), "GOOGLE_API_KEY not set"
assert os.getenv('EMBEDDING_MODEL') == 'gemini-embedding-001', "EMBEDDING_MODEL mismatch"
assert os.getenv('EMBEDDING_DIMENSIONS') == '768', "EMBEDDING_DIMENSIONS mismatch"
assert os.getenv('COLLECTION_NAME') == 'waypoint_kb', "COLLECTION_NAME mismatch"
print("All environment variables OK")
```

**Gemini API Test**:
```python
from google import genai

client = genai.Client()
result = client.models.embed_content(
    model='gemini-embedding-001',
    contents='test embedding'
)
assert len(result.embeddings[0].values) == 768, "Unexpected embedding dimensions"
print(f"Gemini API OK - {len(result.embeddings[0].values)} dimensions")
```

### Constraints
- Virtual environment must be in `venv/` directory (already in `.gitignore`)
- Must use Python 3.11 or higher
- Must work on Windows (primary development platform)
- Must not modify any existing files
- GOOGLE_API_KEY must be set in `.env` for API tests to pass

### Acceptance Criteria
- [ ] `venv/` directory created
- [ ] All packages from `requirements.txt` installed
- [ ] `import chromadb` works
- [ ] `from google import genai` works
- [ ] `import frontmatter` works
- [ ] `from langchain_text_splitters import RecursiveCharacterTextSplitter` works
- [ ] `from dotenv import load_dotenv` works
- [ ] Environment variables load correctly from `.env`
- [ ] Gemini API test returns 768-dimension embedding

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
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Test imports
python -c "import chromadb; print('chromadb OK')"
python -c "from google import genai; print('google-genai OK')"
python -c "import frontmatter; print('frontmatter OK')"
python -c "from langchain_text_splitters import RecursiveCharacterTextSplitter; print('langchain OK')"
python -c "from dotenv import load_dotenv; print('dotenv OK')"

# Test environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'EMBEDDING_MODEL: {os.getenv(\"EMBEDDING_MODEL\")}')"

# Test Gemini API (requires valid GOOGLE_API_KEY)
python -c "from google import genai; c = genai.Client(); r = c.models.embed_content(model='gemini-embedding-001', contents='test'); print(f'Gemini OK - {len(r.embeddings[0].values)} dimensions')"
```

### Expected Output
```
chromadb OK
google-genai OK
frontmatter OK
langchain OK
dotenv OK
EMBEDDING_MODEL: gemini-embedding-001
Gemini OK - 768 dimensions
```

---

## Notes

This task is marked as **optional** because Docker is the primary execution method. However, a local virtual environment is useful for:
- Faster iteration during development
- Debugging without container overhead
- IDE integration (autocomplete, linting)
- Running individual tests

The virtual environment should produce identical results to the Docker container since both use the same `requirements.txt` and `.env` configuration.
