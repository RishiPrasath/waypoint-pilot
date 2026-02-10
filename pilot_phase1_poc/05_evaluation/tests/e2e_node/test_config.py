"""
Test configuration for E2E test suite.
"""

# API Configuration
API_BASE_URL = "http://localhost:3000"
API_QUERY_ENDPOINT = f"{API_BASE_URL}/api/query"
API_HEALTH_ENDPOINT = f"{API_BASE_URL}/api/health"

# Timeouts (in seconds)
DEFAULT_TIMEOUT = 30
SHORT_TIMEOUT = 0.001  # For timeout testing

# Test thresholds
# Increased from 10s to 15s to account for LLM response variability
# See docs/02_e2e_failure_analysis.md for rationale
MAX_LATENCY_MS = 15000  # 15 seconds
MIN_ANSWER_LENGTH = 50  # Minimum characters for valid answer

# Pass rate targets
PASS_RATE_TARGETS = {
    "happy_path": 0.80,      # 80%
    "multi_source": 0.60,    # 60%
    "out_of_scope": 0.80,    # 80%
    "edge_cases": 0.80,      # 80%
    "concurrent": 1.00,      # 100%
    "error_recovery": 1.00,  # 100%
}

# Out-of-scope decline indicators
DECLINE_INDICATORS = [
    "i don't have",
    "i cannot",
    "i'm not able",
    "outside my knowledge",
    "don't have information",
    "cannot provide",
    "not available",
    "beyond my scope",
    "unable to",
    "no information",
    "don't have access",
    "cannot access",
    "real-time",
    "live data",
    "current price",
    "track",
    "booking system",
]
