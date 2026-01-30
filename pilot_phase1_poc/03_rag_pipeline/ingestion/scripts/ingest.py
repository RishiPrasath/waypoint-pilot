"""
Main ingestion script for Waypoint knowledge base.

Orchestrates the full pipeline: discover, parse, chunk, embed, store.
"""

import argparse
import logging
import sys
import time
from typing import Optional

import chromadb
from chromadb.utils import embedding_functions

from scripts.config import (
    CHROMA_PERSIST_PATH,
    COLLECTION_NAME,
    KNOWLEDGE_BASE_PATH,
)
from scripts.process_docs import discover_documents, parse_document
from scripts.chunker import chunk_document

logger = logging.getLogger(__name__)


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: List of arguments (uses sys.argv if None)

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Waypoint Knowledge Base Ingestion Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/ingest.py                    # Full ingestion
  python scripts/ingest.py --dry-run          # Process without storing
  python scripts/ingest.py --verbose          # Show detailed output
  python scripts/ingest.py --category 01_regulatory  # Single category
  python scripts/ingest.py --clear            # Clear and re-ingest
        """
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed chunk information"
    )

    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Process documents without storing to ChromaDB"
    )

    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Only process specific category (e.g., 01_regulatory)"
    )

    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing collection before ingesting"
    )

    return parser.parse_args(args)


def initialize_chromadb():
    """
    Initialize ChromaDB client and collection.

    Returns:
        Tuple of (client, collection)
    """
    # Create persistent client
    client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_PATH))

    # Get default embedding function (all-MiniLM-L6-v2, 384-d)
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    # Get or create collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
        metadata={"description": "Waypoint knowledge base"}
    )

    logger.debug(f"Initialized ChromaDB collection '{COLLECTION_NAME}'")
    return client, collection


def ingest_document(
    doc: dict,
    collection,
    dry_run: bool = False,
    verbose: bool = False
) -> int:
    """
    Ingest a single document into ChromaDB.

    Args:
        doc: Parsed document dict
        collection: ChromaDB collection
        dry_run: If True, don't actually store
        verbose: If True, show chunk details

    Returns:
        Number of chunks ingested
    """
    # Chunk the document
    chunks = chunk_document(doc)

    if verbose:
        for chunk in chunks:
            logger.info(
                f"  Chunk {chunk['chunk_index']}: "
                f"{chunk['chunk_char_count']} chars, "
                f"section='{chunk['section_header'][:30]}...'" if chunk['section_header'] else
                f"  Chunk {chunk['chunk_index']}: {chunk['chunk_char_count']} chars"
            )

    if not dry_run and chunks:
        # Prepare data for ChromaDB
        ids = [chunk["chunk_id"] for chunk in chunks]
        documents = [chunk["chunk_text"] for chunk in chunks]
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
                "source_urls": ",".join(chunk.get("source_urls", [])),
            }
            for chunk in chunks
        ]

        # Add to collection
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        logger.debug(f"Added {len(chunks)} chunks for {doc['doc_id']}")

    return len(chunks)


def run_ingestion(args: argparse.Namespace) -> dict:
    """
    Run the full ingestion pipeline.

    Args:
        args: Parsed command line arguments

    Returns:
        Summary dict with statistics
    """
    start_time = time.time()

    # Initialize results
    results = {
        "documents_processed": 0,
        "documents_failed": 0,
        "chunks_processed": 0,
        "stored": 0,
        "elapsed_time": 0,
        "failed_docs": [],
    }

    # Initialize ChromaDB
    client, collection = initialize_chromadb()

    # Clear collection if requested
    if args.clear and not args.dry_run:
        try:
            # Delete all existing items
            existing = collection.get()
            if existing["ids"]:
                collection.delete(ids=existing["ids"])
                logger.info(f"Cleared {len(existing['ids'])} existing chunks")
        except Exception as e:
            logger.warning(f"Could not clear collection: {e}")

    # Discover documents
    doc_paths = discover_documents(KNOWLEDGE_BASE_PATH)

    # Filter by category if specified
    if args.category:
        doc_paths = [p for p in doc_paths if args.category in str(p)]
        logger.info(f"Filtered to {len(doc_paths)} documents in category '{args.category}'")

    total_docs = len(doc_paths)

    print("\nProcessing documents...")

    # Process each document
    for i, doc_path in enumerate(doc_paths, 1):
        try:
            # Parse document
            doc = parse_document(doc_path)
            doc_id = doc["doc_id"]

            # Ingest
            chunk_count = ingest_document(
                doc,
                collection,
                dry_run=args.dry_run,
                verbose=args.verbose
            )

            results["documents_processed"] += 1
            results["chunks_processed"] += chunk_count

            if not args.dry_run:
                results["stored"] += chunk_count

            # Progress output
            status = "[stored]" if not args.dry_run else "[dry-run]"
            print(f"  [{i}/{total_docs}] {doc_id}: {chunk_count} chunks {status}")

        except Exception as e:
            results["documents_failed"] += 1
            results["failed_docs"].append(str(doc_path))
            logger.error(f"Failed to process {doc_path}: {e}")
            print(f"  [{i}/{total_docs}] {doc_path.name}: FAILED - {e}")

    # Calculate elapsed time
    results["elapsed_time"] = time.time() - start_time

    return results


def print_summary(results: dict, args: argparse.Namespace):
    """Print ingestion summary."""
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    print(f"  Documents processed: {results['documents_processed']}")
    print(f"  Documents failed:    {results['documents_failed']}")
    print(f"  Chunks processed:    {results['chunks_processed']}")

    if args.dry_run:
        print(f"  Stored:              0 (dry-run)")
    else:
        print(f"  Stored:              {results['stored']}")

    print(f"  Time elapsed:        {results['elapsed_time']:.2f}s")

    if results["failed_docs"]:
        print("\nFailed documents:")
        for doc in results["failed_docs"]:
            print(f"  - {doc}")


def main():
    """Main entry point."""
    # Parse arguments
    args = parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(message)s"
    )

    # Print header
    print("\n" + "=" * 50)
    print("Waypoint Ingestion Pipeline")
    print("=" * 50)
    print(f"\nConfiguration:")
    print(f"  Knowledge Base: {KNOWLEDGE_BASE_PATH}")
    print(f"  ChromaDB Path:  {CHROMA_PERSIST_PATH}")
    print(f"  Collection:     {COLLECTION_NAME}")
    print(f"  Dry Run:        {'Yes' if args.dry_run else 'No'}")
    print(f"  Clear:          {'Yes' if args.clear else 'No'}")
    if args.category:
        print(f"  Category:       {args.category}")

    # Run ingestion
    results = run_ingestion(args)

    # Print summary
    print_summary(results, args)

    # Final message
    if not args.dry_run and results["documents_failed"] == 0:
        print(f"\nDone! Collection '{COLLECTION_NAME}' now contains {results['stored']} chunks.")
    elif args.dry_run:
        print(f"\nDry run complete. No data was stored.")

    # Exit with error code if failures
    if results["documents_failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
