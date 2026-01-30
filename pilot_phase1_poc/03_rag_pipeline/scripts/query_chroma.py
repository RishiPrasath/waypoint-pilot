#!/usr/bin/env python3
"""
ChromaDB Query Bridge for Node.js

This script is called from Node.js to perform ChromaDB queries.
It reads query parameters from stdin as JSON and outputs results as JSON.

Usage:
    echo '{"query": "Singapore export", "top_k": 10}' | python query_chroma.py
"""

import json
import sys
from pathlib import Path

# Add ingestion to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'ingestion'))

import chromadb


def query_chroma(query: str, top_k: int = 10, collection_name: str = 'waypoint_kb'):
    """Query ChromaDB and return results."""
    chroma_path = Path(__file__).parent.parent / 'ingestion' / 'chroma_db'

    client = chromadb.PersistentClient(path=str(chroma_path))
    collection = client.get_collection(name=collection_name)

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=['documents', 'metadatas', 'distances']
    )

    # Transform to standard format
    chunks = []
    for i, doc in enumerate(results['documents'][0]):
        chunks.append({
            'content': doc,
            'metadata': results['metadatas'][0][i],
            'distance': results['distances'][0][i],
            'score': 1 - results['distances'][0][i]  # Convert to similarity
        })

    return chunks


def main():
    """Main entry point - reads JSON from stdin, outputs JSON to stdout."""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())

        query = input_data.get('query', '')
        top_k = input_data.get('top_k', 10)
        collection_name = input_data.get('collection_name', 'waypoint_kb')

        if not query:
            print(json.dumps({'error': 'Query is required'}))
            sys.exit(1)

        chunks = query_chroma(query, top_k, collection_name)

        print(json.dumps({
            'success': True,
            'chunks': chunks,
            'count': len(chunks)
        }))

    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e)
        }))
        sys.exit(1)


if __name__ == '__main__':
    main()
