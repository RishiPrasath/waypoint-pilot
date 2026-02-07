"""
Verification script for Waypoint ingestion pipeline.

Validates ChromaDB ingestion quality through 6 progressive checks:
1. Total chunk count (450-520)
2. Category distribution (4/4 categories)
3. Metadata integrity (10/10 fields)
4. Tier 1 retrieval (8/8 category queries)
5. Tier 2 retrieval (10+/12 document queries)
6. Tier 3 scenarios (8+/10 keyword queries)

Forked from 02_ingestion_pipeline/scripts/verify_ingestion.py (Week 1).
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Ensure parent directory is in path for direct script execution
sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb
from chromadb.utils import embedding_functions

from scripts.config import CHROMA_PERSIST_PATH, COLLECTION_NAME


# =============================================================================
# Constants
# =============================================================================

# Expected chunk count range
MIN_CHUNKS = 680
MAX_CHUNKS = 740

# Expected categories
EXPECTED_CATEGORIES = [
    "01_regulatory",
    "02_carriers",
    "03_reference",
    "04_internal_synthetic"
]

# Required metadata fields (10 fields)
REQUIRED_METADATA_FIELDS = [
    "doc_id",
    "title",
    "source_org",
    "source_type",
    "jurisdiction",
    "category",
    "section_header",
    "subsection_header",
    "chunk_index",
    "file_path"
]

# Tier 1 queries: category retrieval (8 queries)
TIER1_QUERIES = [
    ("Singapore Customs import procedures", "01_regulatory"),
    ("Singapore GST customs duty rate", "01_regulatory"),
    ("Maersk shipping services", "02_carriers"),
    ("PIL ocean freight container service", "02_carriers"),
    ("Incoterms FOB explanation", "03_reference"),
    ("HS code classification structure", "03_reference"),
    ("Company SLA policy", "04_internal_synthetic"),
    ("Booking procedure steps", "04_internal_synthetic"),
]

# Tier 2 queries: document retrieval (12 queries)
# Each tuple: (query, list of acceptable doc_id patterns)
TIER2_QUERIES = [
    ("How to import goods into Singapore", ["sg_import"]),
    ("Singapore export documentation", ["sg_export"]),
    ("GST suspended Free Trade Zone", ["ftz", "free_trade"]),
    ("Certificate of Origin Form D", ["certificates_of_origin", "certificate"]),
    ("Indonesia BPOM halal", ["indonesia"]),
    ("ATIGA preferential tariffs", ["atiga", "asean"]),
    ("Maersk transit time", ["maersk"]),
    ("PIL container shipping", ["pil"]),
    ("FOB CIF DDP comparison", ["incoterms"]),
    ("HS code 6 digit structure", ["hs_code"]),
    ("Service level agreement", ["sla"]),
    ("Cash on delivery COD", ["cod"]),
]

# Tier 3 queries: keyword matching (10 queries)
# Each tuple: (query, list of required keywords - at least 2 must be found)
TIER3_QUERIES = [
    ("Documents for FCL export Jakarta", ["invoice", "packing list", "bill of lading"]),
    ("GST rate Singapore 2024", ["9%", "GST", "goods"]),
    ("ASEAN trade agreement benefits", ["ATIGA", "preferential", "tariff"]),
    ("Vietnam import requirements customs", ["Vietnam", "import", "customs"]),
    ("What is FOB incoterms", ["Free On Board", "risk", "seller"]),
    ("Malaysia import permit", ["Malaysia", "permit", "import"]),
    ("Air cargo Singapore", ["cargo", "air", "freight"]),
    ("Escalation customer complaint", ["escalation", "complaint", "manager"]),
    ("Thailand import documentation", ["Thailand", "import", "customs"]),
    ("How to book shipment", ["booking", "shipment", "procedure"]),
]


# =============================================================================
# CLI Argument Parsing
# =============================================================================


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: List of arguments (uses sys.argv if None)

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Waypoint Ingestion Verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m scripts.verify_ingestion              # Run all checks
  python -m scripts.verify_ingestion --verbose    # Detailed output
  python -m scripts.verify_ingestion --tier 1     # Run only tier 1
  python -m scripts.verify_ingestion --check 3    # Run only check 3
        """
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed results"
    )

    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3],
        default=None,
        help="Run only specified tier (1, 2, or 3)"
    )

    parser.add_argument(
        "--check",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        default=None,
        help="Run only specified check (1-6)"
    )

    return parser.parse_args(args)


# =============================================================================
# ChromaDB Initialization
# =============================================================================


def initialize_collection() -> chromadb.Collection:
    """
    Initialize ChromaDB client and return collection.

    Returns:
        ChromaDB collection
    """
    client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_PATH))
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    return collection


# =============================================================================
# Check Functions
# =============================================================================


def check_total_count(collection, verbose: bool = False) -> tuple[bool, str]:
    """
    Check 1: Verify total chunk count is within expected range.

    Args:
        collection: ChromaDB collection
        verbose: Show detailed output

    Returns:
        Tuple of (passed, message)
    """
    count = collection.count()
    passed = MIN_CHUNKS <= count <= MAX_CHUNKS

    if passed:
        message = f"{count} chunks (expected {MIN_CHUNKS}-{MAX_CHUNKS})"
    else:
        message = f"{count} chunks (expected {MIN_CHUNKS}-{MAX_CHUNKS}) - OUT OF RANGE"

    return passed, message


def check_category_distribution(collection, verbose: bool = False) -> tuple[bool, str]:
    """
    Check 2: Verify all 4 categories are present.

    Args:
        collection: ChromaDB collection
        verbose: Show detailed output

    Returns:
        Tuple of (passed, message)
    """
    # Get all metadata to check categories
    result = collection.get(include=["metadatas"])
    metadatas = result.get("metadatas", [])

    if not metadatas:
        return False, "0/4 categories (collection is empty)"

    # Extract unique categories
    found_categories = set()
    for meta in metadatas:
        if meta and "category" in meta:
            found_categories.add(meta["category"])

    # Check which expected categories are present
    present = [cat for cat in EXPECTED_CATEGORIES if cat in found_categories]
    missing = [cat for cat in EXPECTED_CATEGORIES if cat not in found_categories]

    passed = len(present) == len(EXPECTED_CATEGORIES)
    message = f"{len(present)}/4 categories"

    if not passed and missing:
        message += f" (missing: {', '.join(missing)})"

    return passed, message


def check_metadata_integrity(collection, verbose: bool = False) -> tuple[bool, str]:
    """
    Check 3: Verify metadata fields are complete.

    Args:
        collection: ChromaDB collection
        verbose: Show detailed output

    Returns:
        Tuple of (passed, message)
    """
    # Sample chunks to check metadata
    result = collection.get(limit=20, include=["metadatas"])
    metadatas = result.get("metadatas", [])

    if not metadatas:
        return False, "0/10 fields (collection is empty)"

    # Check each sampled chunk for required fields
    all_fields_present = True
    missing_fields_summary = set()

    for meta in metadatas:
        if not meta:
            all_fields_present = False
            continue

        for field in REQUIRED_METADATA_FIELDS:
            if field not in meta:
                all_fields_present = False
                missing_fields_summary.add(field)

    if all_fields_present:
        return True, "10/10 fields"
    else:
        present_count = len(REQUIRED_METADATA_FIELDS) - len(missing_fields_summary)
        message = f"{present_count}/10 fields"
        if missing_fields_summary:
            message += f" (missing: {', '.join(sorted(missing_fields_summary))})"
        return False, message


def check_tier1_retrieval(
    collection,
    verbose: bool = False
) -> tuple[bool, str, int, int]:
    """
    Check 4: Tier 1 category retrieval tests.

    Args:
        collection: ChromaDB collection
        verbose: Show detailed output

    Returns:
        Tuple of (passed, message, pass_count, total)
    """
    total = len(TIER1_QUERIES)
    pass_count = 0
    details = []

    for query, expected_category in TIER1_QUERIES:
        try:
            result = collection.query(
                query_texts=[query],
                n_results=1,
                include=["metadatas"]
            )

            metadatas = result.get("metadatas", [[]])
            if metadatas and metadatas[0]:
                actual_category = metadatas[0][0].get("category", "")
                if actual_category == expected_category:
                    pass_count += 1
                    if verbose:
                        print(f"    [PASS] '{query}' -> {expected_category}")
                else:
                    if verbose:
                        print(
                            f"    [FAIL] '{query}' -> expected {expected_category}, "
                            f"got {actual_category}"
                        )
            else:
                if verbose:
                    print(f"    [FAIL] '{query}' -> no results")

        except Exception as e:
            if verbose:
                print(f"    [FAIL] '{query}' -> error: {e}")

    passed = pass_count == total
    message = f"{pass_count}/{total}"

    return passed, message, pass_count, total


def check_tier2_retrieval(
    collection,
    verbose: bool = False
) -> tuple[bool, str, int, int]:
    """
    Check 5: Tier 2 document retrieval tests.

    Args:
        collection: ChromaDB collection
        verbose: Show detailed output

    Returns:
        Tuple of (passed, message, pass_count, total)
    """
    total = len(TIER2_QUERIES)
    pass_count = 0

    for query, expected_patterns in TIER2_QUERIES:
        try:
            result = collection.query(
                query_texts=[query],
                n_results=3,
                include=["metadatas"]
            )

            metadatas = result.get("metadatas", [[]])
            found = False

            if metadatas and metadatas[0]:
                # Check if any of the top 3 results match expected patterns
                for meta in metadatas[0]:
                    doc_id = meta.get("doc_id", "").lower()
                    for pattern in expected_patterns:
                        if pattern.lower() in doc_id:
                            found = True
                            break
                    if found:
                        break

            if found:
                pass_count += 1
                if verbose:
                    print(f"    [PASS] '{query}'")
            else:
                if verbose:
                    actual_docs = [m.get("doc_id", "?") for m in metadatas[0]] if metadatas[0] else []
                    print(
                        f"    [FAIL] '{query}' -> expected {expected_patterns}, "
                        f"got {actual_docs[:3]}"
                    )

        except Exception as e:
            if verbose:
                print(f"    [FAIL] '{query}' -> error: {e}")

    passed = pass_count >= 10  # 10+ out of 12
    message = f"{pass_count}/{total}"

    return passed, message, pass_count, total


def check_tier3_scenarios(
    collection,
    verbose: bool = False
) -> tuple[bool, str, int, int]:
    """
    Check 6: Tier 3 keyword matching tests.

    Args:
        collection: ChromaDB collection
        verbose: Show detailed output

    Returns:
        Tuple of (passed, message, pass_count, total)
    """
    total = len(TIER3_QUERIES)
    pass_count = 0

    for query, expected_keywords in TIER3_QUERIES:
        try:
            result = collection.query(
                query_texts=[query],
                n_results=3,
                include=["metadatas", "documents"]
            )

            documents = result.get("documents", [[]])

            # Combine text from top results
            combined_text = ""
            if documents and documents[0]:
                combined_text = " ".join(documents[0]).lower()

            # Check if at least 2 keywords are found
            keywords_found = 0
            found_keywords = []
            for keyword in expected_keywords:
                if keyword.lower() in combined_text:
                    keywords_found += 1
                    found_keywords.append(keyword)

            if keywords_found >= 2:
                pass_count += 1
                if verbose:
                    print(f"    [PASS] '{query}' -> found: {found_keywords}")
            else:
                if verbose:
                    print(
                        f"    [FAIL] '{query}' -> found {keywords_found}/3 keywords "
                        f"(need 2+): {found_keywords}"
                    )

        except Exception as e:
            if verbose:
                print(f"    [FAIL] '{query}' -> error: {e}")

    passed = pass_count >= 8  # 8+ out of 10
    message = f"{pass_count}/{total}"

    return passed, message, pass_count, total


# =============================================================================
# Orchestration
# =============================================================================


def run_all_checks(collection, args: argparse.Namespace) -> dict:
    """
    Run all verification checks.

    Args:
        collection: ChromaDB collection
        args: Parsed command line arguments

    Returns:
        Dict with check results
    """
    results = {
        "checks": [],
        "total_passed": 0,
        "total_tests": 0,
        "passed": False
    }

    # Define all checks
    all_checks = [
        (1, None, "Check 1: Total count", check_total_count),
        (2, None, "Check 2: Category distribution", check_category_distribution),
        (3, None, "Check 3: Metadata integrity", check_metadata_integrity),
        (4, 1, "Check 4: Tier 1 retrieval", check_tier1_retrieval),
        (5, 2, "Check 5: Tier 2 retrieval", check_tier2_retrieval),
        (6, 3, "Check 6: Tier 3 scenarios", check_tier3_scenarios),
    ]

    # Filter checks based on args
    checks_to_run = []
    for check_num, tier, name, func in all_checks:
        # If specific check requested
        if args.check is not None and args.check != check_num:
            continue
        # If specific tier requested
        if args.tier is not None:
            if tier is None or tier != args.tier:
                continue
        checks_to_run.append((check_num, tier, name, func))

    # Run selected checks
    for check_num, tier, name, func in checks_to_run:
        if tier is not None:
            # Tier checks return 4 values
            passed, message, pass_count, total = func(collection, args.verbose)
            results["total_passed"] += pass_count
            results["total_tests"] += total
        else:
            # Basic checks return 2 values
            passed, message = func(collection, args.verbose)
            results["total_passed"] += 1 if passed else 0
            results["total_tests"] += 1

        results["checks"].append({
            "name": name,
            "passed": passed,
            "message": message
        })

    # Calculate overall pass
    if results["total_tests"] > 0:
        pass_rate = results["total_passed"] / results["total_tests"]
        results["passed"] = pass_rate >= 0.93  # 93% threshold (28/30)
    else:
        results["passed"] = False

    return results


def print_results(results: dict, verbose: bool = False) -> None:
    """
    Print verification results.

    Args:
        results: Results dict from run_all_checks
        verbose: Show detailed output
    """
    print("\n" + "=" * 50)
    print("Waypoint Ingestion Verification")
    print("=" * 50 + "\n")

    for check in results["checks"]:
        status = "[PASS]" if check["passed"] else "[FAIL]"
        print(f"{status} {check['name']}: {check['message']}")

        if verbose and "details" in check:
            for detail in check["details"]:
                print(detail)

    # Summary
    total = results["total_tests"]
    passed = results["total_passed"]
    pct = (passed / total * 100) if total > 0 else 0

    print(f"\nSummary: {passed}/{total} tests passed ({pct:.0f}%)")

    if results["passed"]:
        print("Result: VERIFICATION PASSED")
    else:
        print("Result: VERIFICATION FAILED")


# =============================================================================
# Main Entry Point
# =============================================================================


def main() -> None:
    """Main entry point."""
    args = parse_args()

    try:
        collection = initialize_collection()
    except Exception as e:
        print(f"Error: Could not initialize collection: {e}")
        print("Have you run the ingestion pipeline first?")
        sys.exit(1)

    results = run_all_checks(collection, args)
    print_results(results, args.verbose)

    # Exit code based on result
    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
