#!/usr/bin/env python3
"""
E2E Test Suite for Waypoint RAG Pipeline

Runs comprehensive end-to-end tests across multiple categories:
- Happy Path: Factual queries with expected good answers
- Multi-Source: Queries requiring multiple documents
- Out-of-Scope: Queries that should be gracefully declined
- Edge Cases: Empty, long, unicode, and injection attempts
- Concurrent: Parallel query execution
- Error Recovery: Timeout and malformed request handling

Usage:
    python scripts/e2e_test_suite.py
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
script_dir = Path(__file__).parent.parent
sys.path.insert(0, str(script_dir))

from tests.e2e.test_config import PASS_RATE_TARGETS
from tests.e2e.test_data import (
    HAPPY_PATH_QUERIES,
    MULTI_SOURCE_QUERIES,
    OUT_OF_SCOPE_QUERIES,
    EDGE_CASE_QUERIES,
    CONCURRENT_QUERIES,
    ERROR_RECOVERY_SCENARIOS,
)
from tests.e2e.test_runner import (
    check_api_health,
    run_happy_path_test,
    run_multi_source_test,
    run_out_of_scope_test,
    run_edge_case_test,
    run_concurrent_tests,
    run_error_recovery_tests,
    calculate_latency_stats,
    TestResult,
)


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_progress(current: int, total: int, test_id: str, passed: bool) -> None:
    """Print test progress."""
    status = "PASS" if passed else "FAIL"
    status_color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"  [{current}/{total}] {test_id}: {status_color}{status}{reset}")


def run_all_tests() -> dict:
    """Run all test categories and return results."""
    results = {
        "happy_path": [],
        "multi_source": [],
        "out_of_scope": [],
        "edge_cases": [],
        "concurrent": [],
        "error_recovery": [],
    }

    # Category A: Happy Path
    print_header("Category A: Happy Path Tests")
    for i, test_case in enumerate(HAPPY_PATH_QUERIES, 1):
        result = run_happy_path_test(test_case)
        results["happy_path"].append(result)
        print_progress(i, len(HAPPY_PATH_QUERIES), result.test_id, result.passed)

    # Category B: Multi-Source
    print_header("Category B: Multi-Source Tests")
    for i, test_case in enumerate(MULTI_SOURCE_QUERIES, 1):
        result = run_multi_source_test(test_case)
        results["multi_source"].append(result)
        print_progress(i, len(MULTI_SOURCE_QUERIES), result.test_id, result.passed)

    # Category C: Out-of-Scope
    print_header("Category C: Out-of-Scope Tests")
    for i, test_case in enumerate(OUT_OF_SCOPE_QUERIES, 1):
        result = run_out_of_scope_test(test_case)
        results["out_of_scope"].append(result)
        print_progress(i, len(OUT_OF_SCOPE_QUERIES), result.test_id, result.passed)

    # Category D: Edge Cases
    print_header("Category D: Edge Case Tests")
    for i, test_case in enumerate(EDGE_CASE_QUERIES, 1):
        result = run_edge_case_test(test_case)
        results["edge_cases"].append(result)
        print_progress(i, len(EDGE_CASE_QUERIES), result.test_id, result.passed)

    # Category E: Concurrent
    print_header("Category E: Concurrent Tests")
    concurrent_results = run_concurrent_tests(CONCURRENT_QUERIES)
    results["concurrent"] = concurrent_results
    for i, result in enumerate(concurrent_results, 1):
        print_progress(i, len(CONCURRENT_QUERIES), result.test_id, result.passed)

    # Category F: Error Recovery
    print_header("Category F: Error Recovery Tests")
    error_results = run_error_recovery_tests(ERROR_RECOVERY_SCENARIOS)
    results["error_recovery"] = error_results
    for i, result in enumerate(error_results, 1):
        print_progress(i, len(ERROR_RECOVERY_SCENARIOS), result.test_id, result.passed)

    return results


def calculate_summary(results: dict) -> dict:
    """Calculate summary statistics for all categories."""
    summary = {}

    for category, category_results in results.items():
        total = len(category_results)
        passed = sum(1 for r in category_results if r.passed)
        failed = total - passed
        pass_rate = passed / total if total > 0 else 0

        summary[category] = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": pass_rate,
            "target": PASS_RATE_TARGETS.get(category, 0.8),
            "meets_target": pass_rate >= PASS_RATE_TARGETS.get(category, 0.8),
        }

    # Calculate totals
    total_tests = sum(s["total"] for s in summary.values())
    total_passed = sum(s["passed"] for s in summary.values())
    total_failed = sum(s["failed"] for s in summary.values())

    summary["total"] = {
        "total": total_tests,
        "passed": total_passed,
        "failed": total_failed,
        "pass_rate": total_passed / total_tests if total_tests > 0 else 0,
    }

    return summary


def generate_report(results: dict, summary: dict, duration: float, report_path: Path) -> None:
    """Generate the markdown test report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Collect all results for latency stats
    all_results = []
    for category_results in results.values():
        all_results.extend(category_results)

    latency_stats = calculate_latency_stats(all_results)

    report = f"""# E2E Test Suite Report

**Date**: {timestamp}
**Duration**: {duration:.1f} seconds
**API Endpoint**: http://localhost:3000/api/query

## Summary

| Category | Total | Passed | Failed | Pass Rate | Target | Status |
|----------|-------|--------|--------|-----------|--------|--------|
| Happy Path | {summary['happy_path']['total']} | {summary['happy_path']['passed']} | {summary['happy_path']['failed']} | {summary['happy_path']['pass_rate']*100:.0f}% | {summary['happy_path']['target']*100:.0f}% | {'✅' if summary['happy_path']['meets_target'] else '❌'} |
| Multi-Source | {summary['multi_source']['total']} | {summary['multi_source']['passed']} | {summary['multi_source']['failed']} | {summary['multi_source']['pass_rate']*100:.0f}% | {summary['multi_source']['target']*100:.0f}% | {'✅' if summary['multi_source']['meets_target'] else '❌'} |
| Out-of-Scope | {summary['out_of_scope']['total']} | {summary['out_of_scope']['passed']} | {summary['out_of_scope']['failed']} | {summary['out_of_scope']['pass_rate']*100:.0f}% | {summary['out_of_scope']['target']*100:.0f}% | {'✅' if summary['out_of_scope']['meets_target'] else '❌'} |
| Edge Cases | {summary['edge_cases']['total']} | {summary['edge_cases']['passed']} | {summary['edge_cases']['failed']} | {summary['edge_cases']['pass_rate']*100:.0f}% | {summary['edge_cases']['target']*100:.0f}% | {'✅' if summary['edge_cases']['meets_target'] else '❌'} |
| Concurrent | {summary['concurrent']['total']} | {summary['concurrent']['passed']} | {summary['concurrent']['failed']} | {summary['concurrent']['pass_rate']*100:.0f}% | {summary['concurrent']['target']*100:.0f}% | {'✅' if summary['concurrent']['meets_target'] else '❌'} |
| Error Recovery | {summary['error_recovery']['total']} | {summary['error_recovery']['passed']} | {summary['error_recovery']['failed']} | {summary['error_recovery']['pass_rate']*100:.0f}% | {summary['error_recovery']['target']*100:.0f}% | {'✅' if summary['error_recovery']['meets_target'] else '❌'} |
| **TOTAL** | **{summary['total']['total']}** | **{summary['total']['passed']}** | **{summary['total']['failed']}** | **{summary['total']['pass_rate']*100:.0f}%** | - | - |

## Performance

| Metric | Value |
|--------|-------|
| Min Latency | {latency_stats['min']:.0f} ms |
| Max Latency | {latency_stats['max']:.0f} ms |
| Avg Latency | {latency_stats['avg']:.0f} ms |
| P95 Latency | {latency_stats['p95']:.0f} ms |

## Detailed Results

### Category A: Happy Path

| # | Query | Status | Latency | Citations | Confidence |
|---|-------|--------|---------|-----------|------------|
"""

    for r in results["happy_path"]:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        query_short = r.query[:40] + "..." if len(r.query) > 40 else r.query
        report += f"| {r.test_id} | {query_short} | {status} | {r.latency_ms:.0f}ms | {r.citation_count} | {r.confidence_level} |\n"

    report += """
### Category B: Multi-Source

| # | Query | Status | Latency | Citations | Confidence |
|---|-------|--------|---------|-----------|------------|
"""

    for r in results["multi_source"]:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        query_short = r.query[:40] + "..." if len(r.query) > 40 else r.query
        report += f"| {r.test_id} | {query_short} | {status} | {r.latency_ms:.0f}ms | {r.citation_count} | {r.confidence_level} |\n"

    report += """
### Category C: Out-of-Scope

| # | Query | Status | Latency | Declined? |
|---|-------|--------|---------|-----------|
"""

    for r in results["out_of_scope"]:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        declined = "Yes" if r.passed else "No (may have hallucinated)"
        report += f"| {r.test_id} | {r.query} | {status} | {r.latency_ms:.0f}ms | {declined} |\n"

    report += """
### Category D: Edge Cases

| # | Description | Status | Latency | Notes |
|---|-------------|--------|---------|-------|
"""

    for r in results["edge_cases"]:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        notes = r.error_message if r.error_message else "Handled OK"
        report += f"| {r.test_id} | {r.description} | {status} | {r.latency_ms:.0f}ms | {notes[:50]} |\n"

    report += """
### Category E: Concurrent

| # | Query | Status | Latency |
|---|-------|--------|---------|
"""

    for r in results["concurrent"]:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        report += f"| {r.test_id} | {r.query} | {status} | {r.latency_ms:.0f}ms |\n"

    report += """
### Category F: Error Recovery

| # | Scenario | Status | Notes |
|---|----------|--------|-------|
"""

    for r in results["error_recovery"]:
        status = "✅ PASS" if r.passed else "❌ FAIL"
        report += f"| {r.test_id} | {r.description} | {status} | {r.error_message[:50] if r.error_message else 'OK'} |\n"

    # Failed tests section
    failed_tests = [r for category_results in results.values() for r in category_results if not r.passed]

    if failed_tests:
        report += """
## Failed Tests

"""
        for r in failed_tests:
            report += f"""### {r.test_id}: {r.description}
- **Category**: {r.category}
- **Query**: {r.query[:100]}{'...' if len(r.query) > 100 else ''}
- **Error**: {r.error_message}
- **Latency**: {r.latency_ms:.0f}ms

"""

    # Recommendations
    report += """
## Recommendations

"""

    if summary["happy_path"]["pass_rate"] < 0.8:
        report += "- ⚠️ Happy path pass rate below target. Review answer generation quality.\n"
    if summary["out_of_scope"]["pass_rate"] < 0.8:
        report += "- ⚠️ Out-of-scope detection needs improvement. Consider refining system prompt.\n"
    if latency_stats["p95"] > 5000:
        report += "- ⚠️ P95 latency is high. Consider caching or optimizing LLM calls.\n"
    if summary["total"]["pass_rate"] >= 0.8:
        report += "- ✅ Overall pass rate meets target. System is ready for further testing.\n"

    report += f"""
---
*Report generated by E2E Test Suite v1.0*
"""

    # Write report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved to: {report_path}")


def print_summary(summary: dict) -> None:
    """Print a summary to console."""
    print_header("Test Summary")

    print(f"\n  {'Category':<15} {'Passed':<8} {'Failed':<8} {'Rate':<8} {'Target':<8} {'Status'}")
    print(f"  {'-'*60}")

    for category in ["happy_path", "multi_source", "out_of_scope", "edge_cases", "concurrent", "error_recovery"]:
        s = summary[category]
        status = "\033[92mOK\033[0m" if s["meets_target"] else "\033[91mFAIL\033[0m"
        print(f"  {category:<15} {s['passed']:<8} {s['failed']:<8} {s['pass_rate']*100:>5.0f}%   {s['target']*100:>5.0f}%   {status}")

    print(f"  {'-'*60}")
    t = summary["total"]
    print(f"  {'TOTAL':<15} {t['passed']:<8} {t['failed']:<8} {t['pass_rate']*100:>5.0f}%")


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("  WAYPOINT RAG PIPELINE - E2E TEST SUITE")
    print("="*60)

    # Check API health
    print("\nChecking API health...")
    healthy, message = check_api_health()
    if not healthy:
        print(f"\033[91mERROR: {message}\033[0m")
        print("\nPlease ensure the backend is running:")
        print("  cd pilot_phase1_poc/03_rag_pipeline && npm start")
        sys.exit(1)

    print(f"\033[92m{message}\033[0m")

    # Run tests
    import time
    start_time = time.time()
    results = run_all_tests()
    duration = time.time() - start_time

    # Calculate summary
    summary = calculate_summary(results)

    # Print summary
    print_summary(summary)

    # Generate report
    report_path = script_dir / "reports" / "e2e_test_report.md"
    generate_report(results, summary, duration, report_path)

    # Exit with appropriate code
    overall_pass = summary["total"]["pass_rate"] >= 0.7  # 70% overall threshold
    print(f"\n{'='*60}")
    if overall_pass:
        print(f"  \033[92mTEST SUITE PASSED\033[0m ({summary['total']['pass_rate']*100:.0f}% pass rate)")
    else:
        print(f"  \033[91mTEST SUITE FAILED\033[0m ({summary['total']['pass_rate']*100:.0f}% pass rate)")
    print(f"  Duration: {duration:.1f}s")
    print(f"{'='*60}\n")

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
