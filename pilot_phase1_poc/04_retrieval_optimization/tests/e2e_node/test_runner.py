"""
Test execution utilities for E2E test suite.
"""

import requests
import time
import statistics
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from .test_config import (
    API_QUERY_ENDPOINT,
    API_HEALTH_ENDPOINT,
    DEFAULT_TIMEOUT,
    SHORT_TIMEOUT,
    MAX_LATENCY_MS,
    MIN_ANSWER_LENGTH,
    DECLINE_INDICATORS,
)


@dataclass
class TestResult:
    """Result of a single test case."""
    test_id: str
    query: str
    description: str
    category: str
    passed: bool
    latency_ms: float = 0
    answer: str = ""
    answer_length: int = 0
    citation_count: int = 0
    matched_citations: int = 0
    confidence_level: str = ""
    error_message: str = ""
    raw_response: dict = field(default_factory=dict)


def check_api_health() -> tuple[bool, str]:
    """Check if the API is healthy and available."""
    try:
        response = requests.get(API_HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            return True, "API is healthy"
        return False, f"API returned status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to API. Is the server running?"
    except Exception as e:
        return False, f"Health check failed: {str(e)}"


def execute_query(query: str, timeout: float = DEFAULT_TIMEOUT) -> tuple[dict | None, float, str | None]:
    """
    Execute a query against the API.

    Returns:
        Tuple of (response_data, latency_ms, error_message)
    """
    start_time = time.time()
    try:
        response = requests.post(
            API_QUERY_ENDPOINT,
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        latency_ms = (time.time() - start_time) * 1000

        if response.status_code == 200:
            return response.json(), latency_ms, None
        else:
            return None, latency_ms, f"HTTP {response.status_code}: {response.text[:200]}"

    except requests.exceptions.Timeout:
        latency_ms = (time.time() - start_time) * 1000
        return None, latency_ms, "Request timed out"
    except requests.exceptions.ConnectionError:
        latency_ms = (time.time() - start_time) * 1000
        return None, latency_ms, "Connection error"
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        return None, latency_ms, str(e)


def execute_malformed_request() -> tuple[bool, str]:
    """Send a malformed request to test error handling."""
    try:
        response = requests.post(
            API_QUERY_ENDPOINT,
            data="this is not valid json{{{",
            headers={"Content-Type": "application/json"},
            timeout=DEFAULT_TIMEOUT,
        )
        # Should get a 400 error, not a 500
        if response.status_code == 400:
            return True, "Properly rejected malformed request with 400"
        elif response.status_code == 500:
            return False, "Server error (500) on malformed request"
        else:
            return True, f"Handled malformed request with status {response.status_code}"
    except Exception as e:
        return False, f"Exception on malformed request: {str(e)}"


def is_decline_response(answer: str) -> bool:
    """Check if the response indicates a graceful decline."""
    answer_lower = answer.lower()
    return any(indicator in answer_lower for indicator in DECLINE_INDICATORS)


def run_happy_path_test(test_case: dict) -> TestResult:
    """Run a happy path test case."""
    response_data, latency_ms, error = execute_query(test_case["query"])

    result = TestResult(
        test_id=test_case["id"],
        query=test_case["query"],
        description=test_case["description"],
        category="happy_path",
        passed=False,
        latency_ms=latency_ms,
    )

    if error:
        result.error_message = error
        return result

    if response_data:
        result.raw_response = response_data
        result.answer = response_data.get("answer", "")
        result.answer_length = len(result.answer)

        citations = response_data.get("citations", [])
        result.citation_count = len(citations)
        result.matched_citations = sum(1 for c in citations if c.get("matched", False))

        confidence = response_data.get("confidence", {})
        result.confidence_level = confidence.get("level", "Unknown")

        # Pass criteria: has answer, within latency limit
        has_answer = result.answer_length >= MIN_ANSWER_LENGTH
        within_latency = latency_ms < MAX_LATENCY_MS

        result.passed = has_answer and within_latency

        if not has_answer:
            result.error_message = f"Answer too short ({result.answer_length} chars)"
        elif not within_latency:
            result.error_message = f"Latency too high ({latency_ms:.0f}ms)"

    return result


def run_multi_source_test(test_case: dict) -> TestResult:
    """Run a multi-source test case."""
    response_data, latency_ms, error = execute_query(test_case["query"])

    result = TestResult(
        test_id=test_case["id"],
        query=test_case["query"],
        description=test_case["description"],
        category="multi_source",
        passed=False,
        latency_ms=latency_ms,
    )

    if error:
        result.error_message = error
        return result

    if response_data:
        result.raw_response = response_data
        result.answer = response_data.get("answer", "")
        result.answer_length = len(result.answer)

        citations = response_data.get("citations", [])
        result.citation_count = len(citations)
        result.matched_citations = sum(1 for c in citations if c.get("matched", False))

        confidence = response_data.get("confidence", {})
        result.confidence_level = confidence.get("level", "Unknown")

        # Pass criteria: has answer (multi-source often needs more time)
        result.passed = result.answer_length >= MIN_ANSWER_LENGTH

        if not result.passed:
            result.error_message = f"Answer too short ({result.answer_length} chars)"

    return result


def run_out_of_scope_test(test_case: dict) -> TestResult:
    """Run an out-of-scope test case."""
    response_data, latency_ms, error = execute_query(test_case["query"])

    result = TestResult(
        test_id=test_case["id"],
        query=test_case["query"],
        description=test_case["description"],
        category="out_of_scope",
        passed=False,
        latency_ms=latency_ms,
    )

    if error:
        result.error_message = error
        return result

    if response_data:
        result.raw_response = response_data
        result.answer = response_data.get("answer", "")
        result.answer_length = len(result.answer)

        confidence = response_data.get("confidence", {})
        result.confidence_level = confidence.get("level", "Unknown")

        # Pass criteria: response indicates decline (not hallucination)
        result.passed = is_decline_response(result.answer)

        if not result.passed:
            result.error_message = "May have hallucinated instead of declining"

    return result


def run_edge_case_test(test_case: dict) -> TestResult:
    """Run an edge case test."""
    response_data, latency_ms, error = execute_query(test_case["query"])

    result = TestResult(
        test_id=test_case["id"],
        query=test_case["query"][:50] + "..." if len(test_case["query"]) > 50 else test_case["query"],
        description=test_case["description"],
        category="edge_cases",
        passed=False,
        latency_ms=latency_ms,
    )

    # For edge cases, we pass if the system doesn't crash
    # Error responses are acceptable as long as they're graceful
    if error:
        # Timeout and connection errors are failures
        if "timed out" in error.lower() or "connection" in error.lower():
            result.error_message = error
            return result
        # HTTP errors (400, 422) are acceptable for invalid input
        result.passed = True
        result.error_message = f"Handled gracefully: {error}"
    elif response_data:
        result.raw_response = response_data
        result.answer = response_data.get("answer", "")
        result.answer_length = len(result.answer)
        result.passed = True  # Got a response without crashing

        confidence = response_data.get("confidence", {})
        result.confidence_level = confidence.get("level", "Unknown")

    return result


def run_concurrent_tests(queries: list[dict]) -> list[TestResult]:
    """Run multiple queries concurrently."""
    results = []

    def execute_concurrent_query(test_case: dict) -> TestResult:
        response_data, latency_ms, error = execute_query(test_case["query"])

        result = TestResult(
            test_id=test_case["id"],
            query=test_case["query"],
            description=test_case["description"],
            category="concurrent",
            passed=False,
            latency_ms=latency_ms,
        )

        if error:
            result.error_message = error
            return result

        if response_data:
            result.raw_response = response_data
            result.answer = response_data.get("answer", "")
            result.answer_length = len(result.answer)
            result.passed = result.answer_length > 0

            if not result.passed:
                result.error_message = "Empty response"

        return result

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(execute_concurrent_query, q): q for q in queries}
        for future in as_completed(futures):
            results.append(future.result())

    return results


def run_error_recovery_tests(scenarios: list[dict]) -> list[TestResult]:
    """Run error recovery tests."""
    results = []

    for scenario in scenarios:
        if scenario["type"] == "timeout":
            # Test with very short timeout
            _, latency_ms, error = execute_query("What is GST?", timeout=SHORT_TIMEOUT)

            result = TestResult(
                test_id=scenario["id"],
                query="Timeout test",
                description=scenario["description"],
                category="error_recovery",
                passed=error is not None and "timed out" in error.lower(),
                latency_ms=latency_ms,
                error_message=error or "No timeout occurred",
            )
            results.append(result)

        elif scenario["type"] == "malformed":
            passed, message = execute_malformed_request()

            result = TestResult(
                test_id=scenario["id"],
                query="Malformed JSON request",
                description=scenario["description"],
                category="error_recovery",
                passed=passed,
                error_message=message,
            )
            results.append(result)

    return results


def calculate_latency_stats(results: list[TestResult]) -> dict:
    """Calculate latency statistics from test results."""
    latencies = [r.latency_ms for r in results if r.latency_ms > 0]

    if not latencies:
        return {
            "min": 0,
            "max": 0,
            "avg": 0,
            "p95": 0,
        }

    sorted_latencies = sorted(latencies)
    p95_index = int(len(sorted_latencies) * 0.95)

    return {
        "min": min(latencies),
        "max": max(latencies),
        "avg": statistics.mean(latencies),
        "p95": sorted_latencies[p95_index] if p95_index < len(sorted_latencies) else sorted_latencies[-1],
    }
