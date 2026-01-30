"""Analyze retrieval test failures."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def main():
    with open(Path(__file__).parent.parent / 'data' / 'retrieval_test_results.json', 'r') as f:
        data = json.load(f)

    # Print all failures
    failures = [r for r in data['all_results'] if not r['hit']]
    print(f'Total failures: {len(failures)}')
    print()
    
    for fail in failures:
        print(f"Query {fail['query_num']}: {fail['query']}")
        print(f"  Category: {fail['category']}")
        print(f"  Expected: {fail['expected_sources']}")
        print(f"  Got: {fail['top_result_doc_id']}")
        print(f"  Score: {fail['top_score']:.3f}")
        print()

if __name__ == "__main__":
    main()
