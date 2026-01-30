"""
Chunking engine for Waypoint knowledge base.

Splits documents into semantic chunks while preserving
metadata and section context for RAG retrieval.
"""

import logging
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

from scripts.config import CHUNK_SIZE, CHUNK_OVERLAP, SEPARATORS

logger = logging.getLogger(__name__)


def generate_chunk_id(doc_id: str, index: int) -> str:
    """
    Generate a unique chunk ID with zero-padded index.

    Args:
        doc_id: The document ID
        index: The chunk index (0-based)

    Returns:
        Chunk ID in format: {doc_id}_chunk_{index:03d}
    """
    return f"{doc_id}_chunk_{index:03d}"


def extract_section_header(content: str, position: int) -> str:
    """
    Extract the most recent ## section header before the given position.

    Args:
        content: Full document content
        position: Character position in content

    Returns:
        Section header text (without ##) or empty string if none found
    """
    # Get content before the position
    text_before = content[:position]

    # Find all ## headers (but not ### headers)
    # Pattern: newline or start, then ## followed by space and text
    pattern = r'(?:^|\n)## ([^\n]+)'
    matches = list(re.finditer(pattern, text_before))

    if matches:
        # Return the last (most recent) match
        return matches[-1].group(1).strip()

    return ""


def extract_subsection_header(content: str, position: int) -> str:
    """
    Extract the most recent ### subsection header before the given position.

    Args:
        content: Full document content
        position: Character position in content

    Returns:
        Subsection header text (without ###) or empty string if none found
    """
    # Get content before the position
    text_before = content[:position]

    # Find all ### headers
    pattern = r'(?:^|\n)### ([^\n]+)'
    matches = list(re.finditer(pattern, text_before))

    if matches:
        # Return the last (most recent) match
        return matches[-1].group(1).strip()

    return ""


def _find_chunk_position(content: str, chunk_text: str, start_from: int = 0) -> int:
    """
    Find the position of a chunk in the original content.

    Args:
        content: Full document content
        chunk_text: The chunk text to find
        start_from: Position to start searching from

    Returns:
        Position of chunk in content, or start_from if not found
    """
    # Try to find the chunk text starting from the last position
    # Use first 100 chars of chunk for matching (handles overlap)
    search_text = chunk_text[:100] if len(chunk_text) > 100 else chunk_text
    pos = content.find(search_text, start_from)

    if pos == -1:
        # Fallback: try without start_from constraint
        pos = content.find(search_text)

    return pos if pos != -1 else start_from


def chunk_document(doc: dict) -> list[dict]:
    """
    Split a document into chunks while preserving metadata.

    Args:
        doc: Parsed document dict from process_docs.parse_document()

    Returns:
        List of chunk dicts with all metadata and chunk-specific fields
    """
    content = doc["content"]
    doc_id = doc["doc_id"]

    # Initialize the text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len,
    )

    # Split the content
    chunk_texts = splitter.split_text(content)

    logger.debug(f"Document {doc_id}: {len(chunk_texts)} chunks")

    # Build chunk objects
    chunks = []
    last_position = 0

    for index, chunk_text in enumerate(chunk_texts):
        # Find position of this chunk in original content
        position = _find_chunk_position(content, chunk_text, last_position)

        # Extract headers at this position
        section_header = extract_section_header(content, position)
        subsection_header = extract_subsection_header(content, position)

        # Build chunk object with all fields
        chunk = {
            # Chunk-specific fields
            "chunk_id": generate_chunk_id(doc_id, index),
            "chunk_index": index,
            "chunk_text": chunk_text,
            "chunk_char_count": len(chunk_text),
            "section_header": section_header,
            "subsection_header": subsection_header,

            # Inherited document fields
            "doc_id": doc["doc_id"],
            "file_path": doc["file_path"],
            "title": doc["title"],
            "source_org": doc["source_org"],
            "source_urls": doc["source_urls"],
            "source_type": doc["source_type"],
            "last_updated": doc["last_updated"],
            "jurisdiction": doc["jurisdiction"],
            "category": doc["category"],
            "use_cases": doc["use_cases"],
            "content": doc["content"],
            "char_count": doc["char_count"],
        }

        chunks.append(chunk)
        last_position = position + len(chunk_text) // 2  # Move past overlap

    logger.info(f"Chunked {doc_id}: {len(chunks)} chunks")
    return chunks


def chunk_all_documents(docs: list[dict]) -> list[dict]:
    """
    Chunk all documents and return a flat list of all chunks.

    Args:
        docs: List of parsed document dicts

    Returns:
        Flat list of all chunk dicts
    """
    all_chunks = []

    for doc in docs:
        try:
            chunks = chunk_document(doc)
            all_chunks.extend(chunks)
        except Exception as e:
            logger.error(f"Failed to chunk {doc['doc_id']}: {e}")

    logger.info(f"Total chunks: {len(all_chunks)} from {len(docs)} documents")
    return all_chunks


if __name__ == "__main__":
    # Quick test when run directly
    import sys
    logging.basicConfig(level=logging.INFO)

    from scripts.process_docs import load_all_documents, parse_document
    from scripts.config import KNOWLEDGE_BASE_PATH

    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        # Test single document
        path = KNOWLEDGE_BASE_PATH / "01_regulatory/singapore_customs/sg_import_procedures.md"
        doc = parse_document(path)
        chunks = chunk_document(doc)

        print(f"Document: {doc['title']}")
        print(f"Content length: {doc['char_count']} chars")
        print(f"Chunks: {len(chunks)}")
        print("-" * 50)

        for i, chunk in enumerate(chunks[:3]):
            print(f"\nChunk {i}:")
            print(f"  ID: {chunk['chunk_id']}")
            print(f"  Section: {chunk['section_header']}")
            print(f"  Subsection: {chunk['subsection_header']}")
            print(f"  Length: {chunk['chunk_char_count']} chars")
            print(f"  Text: {chunk['chunk_text'][:100]}...")
    else:
        # Test all documents
        docs = load_all_documents()
        chunks = chunk_all_documents(docs)

        print(f"\nTotal documents: {len(docs)}")
        print(f"Total chunks: {len(chunks)}")
        print(f"Average chunks/doc: {len(chunks) / len(docs):.1f}")

        # Category distribution
        print("\nChunks by category:")
        categories = {}
        for chunk in chunks:
            cat = chunk["category"]
            categories[cat] = categories.get(cat, 0) + 1

        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")
