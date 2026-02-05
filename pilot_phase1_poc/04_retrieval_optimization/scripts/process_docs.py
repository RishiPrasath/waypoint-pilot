"""
Document processor for Waypoint knowledge base.

Discovers markdown documents, parses YAML frontmatter, and returns
structured document objects ready for chunking and embedding.

The knowledge base is located in 04_retrieval_optimization/kb/ which contains
only content documents (no meta files).

Forked from 02_ingestion_pipeline/scripts/process_docs.py (Week 1).
"""

import logging
from pathlib import Path

import frontmatter

from scripts.config import KNOWLEDGE_BASE_PATH

logger = logging.getLogger(__name__)


def discover_documents(path: Path) -> list[Path]:
    """
    Recursively discover all markdown documents in the knowledge base.

    Args:
        path: Root path to search for documents (kb/ folder)

    Returns:
        Sorted list of Path objects for each document
    """
    documents = list(path.rglob("*.md"))

    # Sort for consistent ordering
    documents.sort()

    logger.info(f"Discovered {len(documents)} documents in {path}")
    return documents


def parse_frontmatter(content: str) -> dict:
    """
    Parse YAML frontmatter from document content.

    Args:
        content: Raw markdown content with potential frontmatter

    Returns:
        Dictionary of frontmatter fields, empty dict if none found
    """
    try:
        post = frontmatter.loads(content)
        return dict(post.metadata)
    except Exception as e:
        logger.warning(f"Failed to parse frontmatter: {e}")
        return {}


def extract_content(content: str) -> str:
    """
    Extract markdown content after frontmatter.

    Args:
        content: Raw markdown content with potential frontmatter

    Returns:
        Clean markdown content without frontmatter
    """
    try:
        post = frontmatter.loads(content)
        return post.content.strip()
    except Exception as e:
        logger.warning(f"Failed to extract content: {e}")
        # Return original content stripped if parsing fails
        return content.strip()


def get_category_from_path(file_path: Path) -> str:
    """
    Extract category from the document's file path.

    Args:
        file_path: Path to the document

    Returns:
        Category name (e.g., '01_regulatory', '02_carriers')
    """
    # Get path relative to knowledge base
    try:
        rel_path = file_path.relative_to(KNOWLEDGE_BASE_PATH)
        # First part is the category folder
        parts = rel_path.parts
        if parts:
            return parts[0]
    except ValueError:
        logger.warning(f"Could not determine category for: {file_path}")

    return "unknown"


def generate_doc_id(file_path: Path) -> str:
    """
    Generate a unique document ID from the file path.

    Args:
        file_path: Path to the document

    Returns:
        Unique ID in format: {category}_{filename}
    """
    category = get_category_from_path(file_path)
    filename = file_path.stem  # filename without extension

    return f"{category}_{filename}"


def _extract_source_urls(source_urls_field) -> list[str]:
    """
    Extract URL strings from the source_urls frontmatter field.

    Handles both simple string lists and nested object structures.

    Args:
        source_urls_field: The source_urls value from frontmatter

    Returns:
        List of URL strings
    """
    if not source_urls_field:
        return []

    urls = []
    for item in source_urls_field:
        if isinstance(item, str):
            urls.append(item)
        elif isinstance(item, dict) and "url" in item:
            urls.append(item["url"])

    return urls


def parse_document(file_path: Path) -> dict:
    """
    Parse a markdown document and return a structured document object.

    Args:
        file_path: Path to the markdown document

    Returns:
        Dictionary with all document fields
    """
    # Read file content
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to read {file_path}: {e}")
        raise

    # Parse frontmatter and content
    metadata = parse_frontmatter(content)
    doc_content = extract_content(content)

    # Build document object with defaults for missing fields
    doc = {
        "doc_id": generate_doc_id(file_path),
        "file_path": str(file_path.resolve()),
        "title": metadata.get("title", file_path.stem.replace("_", " ").title()),
        "source_org": metadata.get("source_organization", ""),
        "source_urls": _extract_source_urls(metadata.get("source_urls", [])),
        "source_type": metadata.get("source_type", "unknown"),
        "last_updated": metadata.get("last_updated", ""),
        "jurisdiction": metadata.get("jurisdiction", ""),
        "category": get_category_from_path(file_path),
        "use_cases": metadata.get("use_cases", []),
        "content": doc_content,
        "char_count": len(doc_content),
    }

    # Convert date to string if it's a date object
    if doc["last_updated"] and not isinstance(doc["last_updated"], str):
        doc["last_updated"] = str(doc["last_updated"])

    logger.debug(f"Parsed document: {doc['doc_id']} ({doc['char_count']} chars)")

    return doc


def load_all_documents() -> list[dict]:
    """
    Load and parse all documents from the knowledge base.

    Returns:
        List of parsed document objects
    """
    documents = []
    failed = []

    doc_paths = discover_documents(KNOWLEDGE_BASE_PATH)

    for doc_path in doc_paths:
        try:
            doc = parse_document(doc_path)
            documents.append(doc)
        except Exception as e:
            logger.error(f"Failed to parse {doc_path}: {e}")
            failed.append(str(doc_path))

    if failed:
        logger.warning(f"Failed to parse {len(failed)} documents: {failed}")

    logger.info(
        f"Loaded {len(documents)} documents, "
        f"total chars: {sum(d['char_count'] for d in documents)}"
    )

    return documents


if __name__ == "__main__":
    # Quick test when run directly
    logging.basicConfig(level=logging.INFO)

    print(f"Knowledge base: {KNOWLEDGE_BASE_PATH}")
    print("-" * 50)

    docs = load_all_documents()

    print(f"\nTotal documents: {len(docs)}")
    print(f"Total characters: {sum(d['char_count'] for d in docs):,}")

    print("\nDocuments by category:")
    categories = {}
    for doc in docs:
        cat = doc["category"]
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    print("\nSample document:")
    if docs:
        sample = docs[0]
        for key, value in sample.items():
            if key == "content":
                print(f"  {key}: ({len(value)} chars)")
            else:
                print(f"  {key}: {value}")
