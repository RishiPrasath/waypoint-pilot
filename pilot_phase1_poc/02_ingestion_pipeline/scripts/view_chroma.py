"""
ChromaDB Viewer - View and explore records in Waypoint knowledge base.

Usage:
    python -m scripts.view_chroma                    # Show summary
    python -m scripts.view_chroma --all              # Show all records
    python -m scripts.view_chroma --limit 10         # Show first 10 records
    python -m scripts.view_chroma --category 01_regulatory  # Filter by category
    python -m scripts.view_chroma --search "customs"  # Search query
    python -m scripts.view_chroma --doc-id sg_import  # Filter by doc_id
"""

import argparse
import json
import sys
from typing import Optional

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import chromadb
from chromadb.utils import embedding_functions

from scripts.config import CHROMA_PERSIST_PATH, COLLECTION_NAME


def get_collection():
    """Initialize and return ChromaDB collection."""
    client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_PATH))
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    return client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)


def show_summary(collection):
    """Show collection summary statistics."""
    count = collection.count()
    result = collection.get(include=["metadatas"])
    metadatas = result.get("metadatas", [])
    
    # Category distribution
    categories = {}
    doc_ids = set()
    sources = set()
    
    for meta in metadatas:
        if meta:
            cat = meta.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
            doc_ids.add(meta.get("doc_id", ""))
            sources.add(meta.get("source_org", ""))
    
    print("\n" + "=" * 60)
    print("ChromaDB Collection Summary")
    print("=" * 60)
    print(f"\nCollection: {COLLECTION_NAME}")
    print(f"Location:   {CHROMA_PERSIST_PATH}")
    print(f"Total Chunks: {count}")
    print(f"Unique Documents: {len(doc_ids)}")
    print(f"Unique Sources: {len(sources)}")
    
    print("\nCategory Distribution:")
    for cat, cnt in sorted(categories.items()):
        print(f"  {cat}: {cnt} chunks")
    
    print("\nDocument IDs:")
    for doc_id in sorted(doc_ids):
        print(f"  - {doc_id}")


def show_records(collection, limit: int = 10, category: Optional[str] = None, 
                 doc_id: Optional[str] = None, show_content: bool = True):
    """Show records with optional filtering."""
    
    # Build where clause
    where = None
    if category:
        where = {"category": category}
    elif doc_id:
        where = {"doc_id": doc_id}
    
    result = collection.get(
        where=where,
        limit=limit,
        include=["documents", "metadatas"]
    )
    
    ids = result.get("ids", [])
    documents = result.get("documents", [])
    metadatas = result.get("metadatas", [])
    
    print(f"\nShowing {len(ids)} records" + (f" (limit: {limit})" if limit else ""))
    print("-" * 60)
    
    for i, (chunk_id, doc, meta) in enumerate(zip(ids, documents, metadatas)):
        print(f"\n[{i+1}] ID: {chunk_id}")
        print(f"    Doc ID: {meta.get('doc_id', 'N/A')}")
        print(f"    Category: {meta.get('category', 'N/A')}")
        print(f"    Title: {meta.get('title', 'N/A')}")
        print(f"    Source: {meta.get('source_org', 'N/A')}")
        print(f"    Section: {meta.get('section_header', 'N/A')}")
        print(f"    Chunk Index: {meta.get('chunk_index', 'N/A')}")
        
        if show_content:
            content_preview = doc[:200] + "..." if len(doc) > 200 else doc
            print(f"    Content: {content_preview}")


def search_records(collection, query: str, n_results: int = 5):
    """Search records using semantic similarity."""
    result = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    
    print(f"\nSearch Results for: '{query}'")
    print(f"Found {len(ids)} results")
    print("-" * 60)
    
    for i, (chunk_id, doc, meta, dist) in enumerate(zip(ids, documents, metadatas, distances)):
        similarity = 1 - dist  # Convert distance to similarity
        print(f"\n[{i+1}] Similarity: {similarity:.4f}")
        print(f"    Doc ID: {meta.get('doc_id', 'N/A')}")
        print(f"    Category: {meta.get('category', 'N/A')}")
        print(f"    Title: {meta.get('title', 'N/A')}")
        print(f"    Section: {meta.get('section_header', 'N/A')}")
        content_preview = doc[:300] + "..." if len(doc) > 300 else doc
        print(f"    Content: {content_preview}")


def export_to_json(collection, filepath: str):
    """Export all records to JSON file."""
    result = collection.get(include=["documents", "metadatas"])
    
    records = []
    for chunk_id, doc, meta in zip(result["ids"], result["documents"], result["metadatas"]):
        records.append({
            "id": chunk_id,
            "content": doc,
            "metadata": meta
        })
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    
    print(f"\nExported {len(records)} records to {filepath}")


def main():
    parser = argparse.ArgumentParser(description="View ChromaDB records")
    parser.add_argument("--all", action="store_true", help="Show all records")
    parser.add_argument("--limit", type=int, default=10, help="Limit number of records")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--doc-id", type=str, help="Filter by document ID")
    parser.add_argument("--search", type=str, help="Semantic search query")
    parser.add_argument("--export", type=str, help="Export to JSON file")
    parser.add_argument("--no-content", action="store_true", help="Hide content in output")
    
    args = parser.parse_args()
    
    try:
        collection = get_collection()
    except Exception as e:
        print(f"Error: Could not open collection: {e}")
        return
    
    if args.export:
        export_to_json(collection, args.export)
    elif args.search:
        search_records(collection, args.search, args.limit)
    elif args.all or args.category or args.doc_id:
        limit = None if args.all else args.limit
        show_records(collection, limit=limit, category=args.category, 
                    doc_id=args.doc_id, show_content=not args.no_content)
    else:
        show_summary(collection)


if __name__ == "__main__":
    main()
