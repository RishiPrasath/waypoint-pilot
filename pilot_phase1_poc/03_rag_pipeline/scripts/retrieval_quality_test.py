"""
Retrieval Quality Test Script

Tests 50 queries against ChromaDB and generates quality reports.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add ingestion scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "ingestion"))

import chromadb
from chromadb.utils import embedding_functions

# Configuration
TOP_K = 5
THRESHOLD = 0.15
CHROMA_PATH = Path(__file__).parent.parent / "ingestion" / "chroma_db"
COLLECTION_NAME = "waypoint_kb"

# Test queries organized by category
TEST_QUERIES = {
    "booking_documentation": [
        "What documents are needed for sea freight Singapore to Indonesia?",
        "How far in advance should I book an LCL shipment?",
        "What's the difference between FCL and LCL?",
        "When is the SI cutoff for this week's Maersk sailing?",
        "Do I need a commercial invoice for samples with no value?",
        "What's a Bill of Lading and who issues it?",
        "Can we ship without a packing list?",
        "What does FOB Singapore mean?",
        "How do I amend a booking after confirmation?",
        "What's the free time at destination port?",
    ],
    "customs_regulatory": [
        "What's the GST rate for imports into Singapore?",
        "How do I find the HS code for electronics?",
        "Is Certificate of Origin required for Thailand?",
        "What permits are needed to import cosmetics to Indonesia?",
        "What's the ATIGA preferential duty rate?",
        "How does the Free Trade Zone work for re-exports?",
        "What's the de minimis threshold for Malaysia?",
        "Do I need halal certification for food to Indonesia?",
        "How do I apply for a Customs ruling on HS code?",
        "What's the difference between Form D and Form AK?",
    ],
    "carrier_information": [
        "Which carriers sail direct to Ho Chi Minh?",
        "What's the transit time to Port Klang?",
        "Does PIL offer reefer containers?",
        "How do I submit VGM to Maersk?",
        "Can I get an electronic Bill of Lading?",
        "What's the weight limit for a 40ft container?",
        "Does ONE service Surabaya?",
        "How do I track my shipment with Evergreen?",
        "What's the difference between Maersk and ONE service?",
        "Who do I contact for a booking amendment?",
    ],
    "sla_service": [
        "What's our standard delivery SLA for Singapore?",
        "Is customs clearance included in door-to-door?",
        "Do you provide cargo insurance?",
        "What happens if shipment is delayed?",
        "Are duties and taxes included in the quote?",
        "What's the process for refused deliveries?",
        "Do you handle import permit applications?",
        "How do I upgrade to express service?",
        "What's covered under standard liability?",
        "Can I get proof of delivery?",
    ],
    "edge_cases_out_of_scope": [
        "What's the current freight rate to Jakarta?",
        "Where is my shipment right now?",
        "Can you book a shipment for me?",
        "I want to file a claim for damaged cargo",
        "Can you ship hazmat by air?",
        "What's the weather forecast for shipping?",
        "Can you recommend a supplier in China?",
        "What's your company's financial status?",
        "How do I become a freight forwarder?",
        "What are your competitor's rates?",
    ],
}

# Expected document keywords for hit rate calculation
# Maps query keywords to expected doc_id substrings
EXPECTED_SOURCES = {
    # Booking queries
    "What documents are needed for sea freight Singapore to Indonesia?": ["sg_export", "indonesia_import"],
    "How far in advance should I book an LCL shipment?": ["booking"],
    "What's the difference between FCL and LCL?": ["incoterms"],
    "When is the SI cutoff for this week's Maersk sailing?": ["maersk"],
    "Do I need a commercial invoice for samples with no value?": ["sg_export", "indonesia_import"],
    "What's a Bill of Lading and who issues it?": ["booking"],
    "Can we ship without a packing list?": ["sg_export", "indonesia_import"],
    "What does FOB Singapore mean?": ["incoterms"],
    "How do I amend a booking after confirmation?": ["booking"],
    "What's the free time at destination port?": ["carrier", "service"],
    # Customs queries
    "What's the GST rate for imports into Singapore?": ["sg_gst"],
    "How do I find the HS code for electronics?": ["hs_classification", "hs_code"],
    "Is Certificate of Origin required for Thailand?": ["sg_certificates", "atiga"],
    "What permits are needed to import cosmetics to Indonesia?": ["indonesia_import"],
    "What's the ATIGA preferential duty rate?": ["atiga"],
    "How does the Free Trade Zone work for re-exports?": ["sg_free_trade"],
    "What's the de minimis threshold for Malaysia?": ["malaysia_import"],
    "Do I need halal certification for food to Indonesia?": ["indonesia_import"],
    "How do I apply for a Customs ruling on HS code?": ["sg_hs_classification"],
    "What's the difference between Form D and Form AK?": ["asean_rules", "atiga"],
    # Carrier queries
    "Which carriers sail direct to Ho Chi Minh?": ["pil", "maersk", "one", "evergreen"],
    "What's the transit time to Port Klang?": ["pil", "maersk", "one", "evergreen"],
    "Does PIL offer reefer containers?": ["pil"],
    "How do I submit VGM to Maersk?": ["maersk"],
    "Can I get an electronic Bill of Lading?": ["carrier", "maersk", "evergreen"],
    "What's the weight limit for a 40ft container?": ["carrier"],
    "Does ONE service Surabaya?": ["one"],
    "How do I track my shipment with Evergreen?": ["evergreen"],
    "What's the difference between Maersk and ONE service?": ["maersk", "one"],
    "Who do I contact for a booking amendment?": ["booking", "escalation"],
    # SLA queries
    "What's our standard delivery SLA for Singapore?": ["sla_policy"],
    "Is customs clearance included in door-to-door?": ["service_terms", "sla_policy"],
    "Do you provide cargo insurance?": ["service_terms"],
    "What happens if shipment is delayed?": ["sla_policy", "escalation"],
    "Are duties and taxes included in the quote?": ["service_terms"],
    "What's the process for refused deliveries?": ["cod_procedure", "service_terms"],
    "Do you handle import permit applications?": ["service_terms", "booking"],
    "How do I upgrade to express service?": ["service_terms", "booking"],
    "What's covered under standard liability?": ["service_terms", "sla_policy"],
    "Can I get proof of delivery?": ["cod_procedure", "service_terms"],
    # Edge cases - these should return low scores or irrelevant docs
    "What's the current freight rate to Jakarta?": [],  # Out of scope
    "Where is my shipment right now?": [],  # Out of scope
    "Can you book a shipment for me?": [],  # Out of scope
    "I want to file a claim for damaged cargo": [],  # Out of scope
    "Can you ship hazmat by air?": [],  # Out of scope
    "What's the weather forecast for shipping?": [],  # Out of scope
    "Can you recommend a supplier in China?": [],  # Out of scope
    "What's your company's financial status?": [],  # Out of scope
    "How do I become a freight forwarder?": [],  # Out of scope
    "What are your competitor's rates?": [],  # Out of scope
}


def initialize_chromadb():
    """Initialize ChromaDB client and collection."""
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )
    return collection


def run_query(collection, query: str, top_k: int = TOP_K) -> list[dict]:
    """Run a single query and return results with scores."""
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["metadatas", "documents", "distances"]
    )
    
    chunks = []
    for i in range(len(results["ids"][0])):
        # Convert distance to similarity score (1 - distance)
        distance = results["distances"][0][i]
        similarity = 1 - distance
        
        chunks.append({
            "chunk_id": results["ids"][0][i],
            "metadata": results["metadatas"][0][i],
            "text": results["documents"][0][i][:200] + "..." if len(results["documents"][0][i]) > 200 else results["documents"][0][i],
            "similarity": round(similarity, 4),
        })
    
    return chunks


def is_hit(chunks: list[dict], expected_keywords: list[str]) -> bool:
    """Check if any of the top-3 chunks match expected source keywords."""
    if not expected_keywords:
        # For out-of-scope queries, we expect no good matches
        # Consider it a "hit" if top score is below threshold
        return chunks[0]["similarity"] < THRESHOLD if chunks else True
    
    for chunk in chunks[:3]:  # Check top 3
        doc_id = chunk["metadata"].get("doc_id", "").lower()
        for keyword in expected_keywords:
            if keyword.lower() in doc_id:
                return True
    return False


def get_matching_source(chunk: dict, expected_keywords: list[str]) -> Optional[str]:
    """Get the matching source keyword for a chunk."""
    doc_id = chunk["metadata"].get("doc_id", "").lower()
    for keyword in expected_keywords:
        if keyword.lower() in doc_id:
            return keyword
    return None


def run_all_tests(collection) -> dict:
    """Run all 50 test queries and collect results."""
    all_results = []
    category_stats = {}
    
    total_queries = sum(len(queries) for queries in TEST_QUERIES.values())
    query_num = 0
    
    print(f"\nRunning retrieval quality tests...")
    print(f"Total queries: {total_queries}")
    print(f"Top-K: {TOP_K}, Threshold: {THRESHOLD}")
    print("=" * 60)
    
    for category, queries in TEST_QUERIES.items():
        print(f"\nTesting {category} ({len(queries)} queries)...")
        
        category_hits = 0
        category_results = []
        
        for i, query in enumerate(queries, 1):
            query_num += 1
            chunks = run_query(collection, query)
            expected = EXPECTED_SOURCES.get(query, [])
            hit = is_hit(chunks, expected)
            
            if hit:
                category_hits += 1
            
            # Find which source matched (if any)
            matched_source = None
            if hit and expected:
                for chunk in chunks[:3]:
                    matched_source = get_matching_source(chunk, expected)
                    if matched_source:
                        break
            
            result = {
                "query_num": query_num,
                "category": category,
                "query": query,
                "top_result_doc_id": chunks[0]["metadata"]["doc_id"] if chunks else None,
                "top_result_title": chunks[0]["metadata"]["title"] if chunks else None,
                "top_score": chunks[0]["similarity"] if chunks else 0,
                "hit": hit,
                "expected_sources": expected,
                "matched_source": matched_source,
                "top_5_chunks": [
                    {
                        "doc_id": c["metadata"]["doc_id"],
                        "title": c["metadata"]["title"],
                        "section": c["metadata"].get("section_header", ""),
                        "similarity": c["similarity"],
                    }
                    for c in chunks
                ]
            }
            
            category_results.append(result)
            all_results.append(result)
            
            status = "PASS" if hit else "FAIL"
            print(f"  [{i}/{len(queries)}] \"{query[:50]}...\" -> {chunks[0]['metadata']['doc_id'][:30]} ({chunks[0]['similarity']:.2f}) {status}")
        
        hit_rate = (category_hits / len(queries)) * 100
        category_stats[category] = {
            "queries": len(queries),
            "hits": category_hits,
            "hit_rate": round(hit_rate, 1),
            "results": category_results,
        }
        
        print(f"  Category hit rate: {hit_rate:.1f}%")
    
    # Calculate overall stats
    total_hits = sum(stats["hits"] for stats in category_stats.values())
    overall_hit_rate = (total_hits / total_queries) * 100
    
    return {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "top_k": TOP_K,
            "threshold": THRESHOLD,
            "chroma_path": str(CHROMA_PATH),
            "collection_name": COLLECTION_NAME,
        },
        "summary": {
            "total_queries": total_queries,
            "total_hits": total_hits,
            "overall_hit_rate": round(overall_hit_rate, 1),
        },
        "category_stats": category_stats,
        "all_results": all_results,
    }


def determine_decision(overall_hit_rate: float) -> str:
    """Determine decision based on hit rate."""
    if overall_hit_rate >= 75:
        return "PROCEED"
    elif overall_hit_rate >= 60:
        return "INVESTIGATE"
    else:
        return "REMEDIATE"


def generate_json_report(results: dict, output_path: Path):
    """Save raw results to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nJSON report saved: {output_path}")


def generate_markdown_report(results: dict, output_path: Path):
    """Generate human-readable markdown report."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    summary = results["summary"]
    category_stats = results["category_stats"]
    decision = determine_decision(summary["overall_hit_rate"])
    
    md = f"""# Retrieval Quality Report

**Generated**: {results["timestamp"]}
**Total Queries**: {summary["total_queries"]}
**Top-K**: {results["config"]["top_k"]}
**Threshold**: {results["config"]["threshold"]}

## Summary

| Category | Queries | Hits (Top-3) | Hit Rate |
|----------|---------|--------------|----------|
"""
    
    for category, stats in category_stats.items():
        category_name = category.replace("_", " ").title()
        md += f"| {category_name} | {stats['queries']} | {stats['hits']} | {stats['hit_rate']}% |\n"
    
    md += f"| **TOTAL** | **{summary['total_queries']}** | **{summary['total_hits']}** | **{summary['overall_hit_rate']}%** |\n"
    
    md += f"""
## Decision Gate

| Quality Level | Threshold | Action |
|---------------|-----------|--------|
| ≥75% | PROCEED | Build retrieval service |
| 60-74% | INVESTIGATE | Review failures, minor fixes |
| <60% | REMEDIATE | Chunking optimization needed |

**Result**: **{decision}** (Hit rate: {summary['overall_hit_rate']}%)

"""
    
    # Top 10 failures
    failures = [r for r in results["all_results"] if not r["hit"]]
    failures.sort(key=lambda x: x["top_score"], reverse=True)
    top_failures = failures[:10]
    
    md += "## Top 10 Failures\n\n"
    md += "| Query | Expected | Got | Score |\n"
    md += "|-------|----------|-----|-------|\n"
    
    for f in top_failures:
        query_short = f["query"][:50] + "..." if len(f["query"]) > 50 else f["query"]
        expected = ", ".join(f["expected_sources"]) if f["expected_sources"] else "(out-of-scope)"
        got = f["top_result_doc_id"][:40] if f["top_result_doc_id"] else "None"
        md += f"| {query_short} | {expected} | {got} | {f['top_score']:.3f} |\n"
    
    # Per-category details
    md += "\n## Per-Category Details\n"
    
    for category, stats in category_stats.items():
        category_name = category.replace("_", " ").title()
        md += f"\n### {category_name}\n\n"
        md += "| # | Query | Top Result | Score | Hit? |\n"
        md += "|---|-------|------------|-------|------|\n"
        
        for r in stats["results"]:
            query_short = r["query"][:45] + "..." if len(r["query"]) > 45 else r["query"]
            top_result = r["top_result_doc_id"][:35] if r["top_result_doc_id"] else "None"
            hit_mark = "PASS" if r["hit"] else "FAIL"
            md += f"| {r['query_num']} | {query_short} | {top_result} | {r['top_score']:.3f} | {hit_mark} |\n"
    
    # Full results appendix
    md += "\n## Appendix: Full Results\n\n"
    md += "```json\n"
    md += json.dumps(results["all_results"], indent=2)[:3000]  # Truncate for readability
    md += "\n... (truncated)\n"
    md += "```\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"Markdown report saved: {output_path}")


def main():
    """Run all tests and generate reports."""
    print("=" * 60)
    print("Waypoint Retrieval Quality Test")
    print("=" * 60)
    
    # Initialize ChromaDB
    try:
        collection = initialize_chromadb()
        print(f"\nConnected to ChromaDB: {CHROMA_PATH}")
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Total chunks: {collection.count()}")
    except Exception as e:
        print(f"Error connecting to ChromaDB: {e}")
        sys.exit(1)
    
    # Run all tests
    results = run_all_tests(collection)
    
    # Generate reports
    project_root = Path(__file__).parent.parent
    json_path = project_root / "data" / "retrieval_test_results.json"
    md_path = project_root / "reports" / "retrieval_quality_REPORT.md"
    
    generate_json_report(results, json_path)
    generate_markdown_report(results, md_path)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total queries: {results['summary']['total_queries']}")
    print(f"Overall hit rate: {results['summary']['overall_hit_rate']}%")
    print(f"Decision: {determine_decision(results['summary']['overall_hit_rate'])}")
    print("\nReports generated:")
    print(f"  - {json_path}")
    print(f"  - {md_path}")


if __name__ == "__main__":
    main()
