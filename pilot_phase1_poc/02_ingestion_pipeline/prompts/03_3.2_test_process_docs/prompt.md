# Task 3.2: Test Document Processor Module

## Persona

> You are a Python test engineer specializing in TDD and pytest.
> You write comprehensive, readable tests with clear arrange-act-assert structure.
> You prioritize edge cases, error handling, and meaningful assertions.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The document processor module (`scripts/process_docs.py`) was created in Task 3.1 and needs comprehensive test coverage before proceeding to the chunking engine.

### Current State
- ✅ `scripts/process_docs.py` exists with 7 public functions
- ✅ `tests/__init__.py` exists
- ✅ pytest installed (v9.0.2)
- 📁 Knowledge base at `01_knowledge_base/kb/` has 29 documents across 4 categories

**Note**: The `kb/` folder contains ONLY content documents (no exclusions needed).

### Reference Documents
- Module under test: `scripts/process_docs.py`
- Config: `scripts/config.py`
- Roadmap: `docs/01_implementation_roadmap.md`

### Dependencies
- Task 3.1 (process_docs.py) ✅ Complete

---

## Task

### Objective
Create comprehensive pytest test suite for `scripts/process_docs.py` covering all public functions, edge cases, and error handling.

### Requirements

1. **Test file**: `tests/test_process_docs.py`

2. **Test coverage for all public functions**:
   - `discover_documents(path)`
   - `parse_frontmatter(content)`
   - `extract_content(content)`
   - `get_category_from_path(file_path)`
   - `generate_doc_id(file_path)`
   - `parse_document(file_path)`
   - `load_all_documents()`

3. **Test categories**:
   - Happy path tests (normal operation)
   - Edge case tests (missing fields, empty content)
   - Integration tests (real knowledge base documents)

### Test Specifications

#### 1. `test_discover_documents`
```python
class TestDiscoverDocuments:
    def test_finds_all_29_documents(self):
        """Should discover exactly 29 content documents from kb/ folder."""

    def test_returns_sorted_paths(self):
        """Should return paths in sorted order."""

    def test_returns_path_objects(self):
        """Should return list of Path objects."""

    def test_all_files_are_markdown(self):
        """All discovered files should have .md extension."""
```

#### 2. `test_parse_frontmatter`
```python
class TestParseFrontmatter:
    def test_parses_valid_yaml(self):
        """Should parse valid YAML frontmatter."""

    def test_returns_empty_dict_for_no_frontmatter(self):
        """Should return {} for content without frontmatter."""

    def test_handles_nested_source_urls(self):
        """Should parse nested source_urls structure."""

    def test_handles_list_fields(self):
        """Should parse use_cases as list."""
```

#### 3. `test_extract_content`
```python
class TestExtractContent:
    def test_removes_frontmatter(self):
        """Should return content without YAML block."""

    def test_strips_whitespace(self):
        """Should strip leading/trailing whitespace."""

    def test_handles_no_frontmatter(self):
        """Should return original content if no frontmatter."""
```

#### 4. `test_get_category_from_path`
```python
class TestGetCategoryFromPath:
    def test_extracts_regulatory_category(self):
        """Should extract '01_regulatory' from path."""

    def test_extracts_carriers_category(self):
        """Should extract '02_carriers' from path."""

    def test_extracts_reference_category(self):
        """Should extract '03_reference' from path."""

    def test_extracts_internal_category(self):
        """Should extract '04_internal_synthetic' from path."""
```

#### 5. `test_generate_doc_id`
```python
class TestGenerateDocId:
    def test_creates_unique_id(self):
        """Should create ID in format: {category}_{filename}."""

    def test_excludes_file_extension(self):
        """Should not include .md in doc_id."""
```

#### 6. `test_parse_document`
```python
class TestParseDocument:
    def test_returns_all_12_fields(self):
        """Should return dict with all 12 required fields."""

    def test_maps_source_organization_to_source_org(self):
        """Should map source_organization → source_org."""

    def test_extracts_urls_from_nested_objects(self):
        """Should extract url field from nested source_urls."""

    def test_handles_missing_optional_fields(self):
        """Should use defaults for missing fields."""

    def test_calculates_char_count(self):
        """Should include accurate char_count."""
```

#### 7. `test_load_all_documents`
```python
class TestLoadAllDocuments:
    def test_loads_all_29_documents(self):
        """Should load exactly 29 documents."""

    def test_all_documents_have_required_fields(self):
        """Each document should have all 12 fields."""

    def test_total_char_count_reasonable(self):
        """Total chars should be ~185,000."""

    def test_category_distribution(self):
        """Should have correct count per category."""
```

### Fixtures

```python
@pytest.fixture
def sample_frontmatter_content():
    """Sample markdown with valid frontmatter."""
    return '''---
title: Test Document
source_organization: Test Org
source_urls:
  - url: https://example.com
    description: Test URL
source_type: public_regulatory
last_updated: 2025-01-26
jurisdiction: SG
category: customs
use_cases: [UC-1.1, UC-2.1]
---

# Test Content

This is test content.
'''

@pytest.fixture
def sample_no_frontmatter():
    """Sample markdown without frontmatter."""
    return '''# Just Content

No frontmatter here.
'''

@pytest.fixture
def real_document_path():
    """Path to a real document in knowledge base (kb/ folder)."""
    from scripts.config import KNOWLEDGE_BASE_PATH
    return KNOWLEDGE_BASE_PATH / "01_regulatory/singapore_customs/sg_import_procedures.md"
```

### Constraints
- Tests must be independent (no shared state)
- Use fixtures for reusable test data
- Real file tests should use actual knowledge base documents
- Don't mock the file system for integration tests

### Acceptance Criteria
- [ ] Test file created at `tests/test_process_docs.py`
- [ ] All 7 public functions have test coverage
- [ ] Tests include happy path and edge cases
- [ ] All tests pass with `pytest tests/test_process_docs.py -v`
- [ ] At least 20 test cases total

### TDD Requirements
- [ ] Test file created at `tests/test_process_docs.py`
- [ ] Tests written covering all public functions
- [ ] All tests pass

---

## Format

### Output Structure
```
tests/
├── __init__.py
└── test_process_docs.py    # New file
```

### Code Style
- Python 3.11+ type hints where helpful
- pytest style (no unittest.TestCase)
- Class-based grouping by function under test
- Descriptive test names: `test_<scenario>_<expected>`
- Docstrings explaining what each test verifies

### Test Structure
```python
"""
Tests for scripts/process_docs.py
"""

import pytest
from pathlib import Path

from scripts.process_docs import (
    discover_documents,
    parse_frontmatter,
    extract_content,
    get_category_from_path,
    generate_doc_id,
    parse_document,
    load_all_documents,
)
from scripts.config import KNOWLEDGE_BASE_PATH


# Fixtures
@pytest.fixture
def sample_frontmatter_content():
    ...


# Test Classes
class TestDiscoverDocuments:
    def test_finds_all_29_documents(self):
        # Arrange
        path = KNOWLEDGE_BASE_PATH

        # Act
        docs = discover_documents(path)

        # Assert
        assert len(docs) == 29

    ...
```

### Validation
```bash
# Run all process_docs tests
python -m pytest tests/test_process_docs.py -v

# Run with coverage
python -m pytest tests/test_process_docs.py --cov=scripts.process_docs --cov-report=term-missing

# Run specific test class
python -m pytest tests/test_process_docs.py::TestDiscoverDocuments -v
```

---

## Execution Checklist

After implementing, verify:
1. [ ] All tests pass: `pytest tests/test_process_docs.py -v`
2. [ ] At least 20 test cases
3. [ ] Coverage for all 7 public functions
4. [ ] No skipped or xfailed tests
5. [ ] Tests run in < 5 seconds
