"""
Evaluation Harness for Waypoint Co-Pilot
Sends 50 queries to the live API, checks answers against baselines,
and generates evaluation reports.

Usage:
  python scripts/evaluation_harness.py
  python scripts/evaluation_harness.py --delay 10
  python scripts/evaluation_harness.py --start-from Q-15
  python scripts/evaluation_harness.py --dry-run

Environment:
  EVAL_DELAY_SECONDS  - delay between queries (default: 30)
  EVAL_API_URL        - API base URL (default: http://localhost:3000)
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_DELAY = int(os.environ.get("EVAL_DELAY_SECONDS", "30"))
DEFAULT_API_URL = os.environ.get("EVAL_API_URL", "http://localhost:3000")
QUERY_ENDPOINT = "/api/query"
REQUEST_TIMEOUT = 30  # seconds
LATENCY_THRESHOLD_MS = 5000
MAX_RETRIES = 3

# Paths relative to 05_evaluation/
BASE_DIR = Path(__file__).resolve().parent.parent
BASELINES_PATH = BASE_DIR / "data" / "evaluation_baselines.json"
RESULTS_JSON_PATH = BASE_DIR / "data" / "evaluation_results.json"
RESULTS_CSV_PATH = BASE_DIR / "data" / "evaluation_results.csv"
REPORT_MD_PATH = BASE_DIR / "reports" / "evaluation_report.md"

# Week 4 targets
TARGETS = {
    "deflection_rate": 40.0,
    "citation_accuracy": 80.0,
    "hallucination_rate": 15.0,  # must be BELOW this
    "oos_handling_rate": 90.0,
    "avg_latency_ms": 5000.0,   # must be BELOW this
}


# ---------------------------------------------------------------------------
# Step 1: Load Baselines
# ---------------------------------------------------------------------------

def load_baselines(path: str = None) -> list:
    """Load and validate evaluation_baselines.json."""
    p = Path(path) if path else BASELINES_PATH
    if not p.exists():
        print(f"ERROR: Baselines file not found: {p}")
        sys.exit(1)

    with open(p, encoding="utf-8") as f:
        data = json.load(f)

    queries = data.get("queries", [])
    if len(queries) != 50:
        print(f"WARNING: Expected 50 queries, got {len(queries)}")

    # Validate required fields
    required = ["id", "category", "query", "is_oos", "expected_docs",
                "must_contain", "must_not_contain"]
    for q in queries:
        for field in required:
            if field not in q:
                print(f"ERROR: Query {q.get('id', '?')} missing field: {field}")
                sys.exit(1)

    # Sort by id
    queries.sort(key=lambda q: q["id"])
    print(f"Loaded {len(queries)} baselines (version: {data.get('version', '?')})")
    return queries


# ---------------------------------------------------------------------------
# Step 2: Send Queries
# ---------------------------------------------------------------------------

def send_query(api_url: str, query: str) -> dict:
    """Send a single query to POST /api/query."""
    url = f"{api_url}{QUERY_ENDPOINT}"
    start = time.time()

    try:
        resp = requests.post(
            url,
            json={"query": query},
            timeout=REQUEST_TIMEOUT,
        )
        latency_ms = int((time.time() - start) * 1000)

        if resp.status_code == 429:
            return {
                "response": None,
                "latency_ms": latency_ms,
                "status_code": 429,
                "error": "Rate limited (429)",
            }

        if resp.status_code != 200:
            return {
                "response": None,
                "latency_ms": latency_ms,
                "status_code": resp.status_code,
                "error": f"HTTP {resp.status_code}: {resp.text[:200]}",
            }

        return {
            "response": resp.json(),
            "latency_ms": latency_ms,
            "status_code": 200,
            "error": None,
        }

    except requests.exceptions.ConnectionError:
        return {
            "response": None,
            "latency_ms": int((time.time() - start) * 1000),
            "status_code": 0,
            "error": f"Connection refused - backend not running on {api_url}",
        }
    except requests.exceptions.Timeout:
        return {
            "response": None,
            "latency_ms": int((time.time() - start) * 1000),
            "status_code": 0,
            "error": f"Timeout after {REQUEST_TIMEOUT}s",
        }
    except Exception as e:
        return {
            "response": None,
            "latency_ms": int((time.time() - start) * 1000),
            "status_code": 0,
            "error": str(e),
        }


def run_all_queries(baselines: list, api_url: str, delay: int,
                    start_from: str = "Q-01") -> list:
    """Send all queries sequentially with delay between each."""
    results = []
    total = len(baselines)
    skipping = True if start_from != "Q-01" else False

    for i, baseline in enumerate(baselines):
        qid = baseline["id"]

        # Skip until start_from
        if skipping:
            if qid == start_from:
                skipping = False
            else:
                continue

        query_text = baseline["query"]
        short_query = query_text[:55] + "..." if len(query_text) > 55 else query_text
        print(f"  [{i+1:02d}/{total}] {qid}: \"{short_query}\"", end=" ", flush=True)

        # Send with retry on 429
        result = None
        for retry in range(MAX_RETRIES + 1):
            result = send_query(api_url, query_text)

            if result["status_code"] == 0 and "Connection refused" in (result["error"] or ""):
                print(f"\n\nERROR: {result['error']}")
                print("Start the backend with: cd pilot_phase1_poc/05_evaluation && npm start")
                # Save partial results
                if results:
                    print(f"\nSaving {len(results)} partial results...")
                return results

            if result["status_code"] != 429:
                break

            backoff = delay * (2 ** retry)
            print(f"(429 - backoff {backoff}s)", end=" ", flush=True)
            time.sleep(backoff)

        # Log result
        if result["error"]:
            print(f"({result['latency_ms']}ms) FAIL {result['error']}")
        else:
            confidence = result["response"].get("confidence", {}).get("level", "?")
            latency = result["response"].get("metadata", {}).get("latencyMs", result["latency_ms"])
            print(f"({latency}ms) [{confidence}] PASS")

        # Run checks
        checks = run_checks(baseline, result)
        overall = all(c["pass"] for c in checks.values() if c.get("applicable", True))

        results.append({
            "id": qid,
            "category": baseline["category"],
            "query": query_text,
            "is_oos": baseline["is_oos"],
            "response": result["response"],
            "checks": checks,
            "overall_pass": overall,
            "client_latency_ms": result["latency_ms"],
            "error": result["error"],
        })

        # Delay between requests (skip after last query)
        if i < total - 1 and not skipping:
            remaining = total - i - 1
            if delay > 0 and remaining > 0:
                time.sleep(delay)

    return results


# ---------------------------------------------------------------------------
# Step 3: Automated Checks
# ---------------------------------------------------------------------------

def check_must_contain(answer: str, keywords: list) -> dict:
    """Check if answer contains all required keywords (case-insensitive)."""
    if not keywords:
        return {"pass": True, "total": 0, "matched": 0, "missing": []}

    answer_lower = answer.lower()
    matched = []
    missing = []
    for kw in keywords:
        if kw.lower() in answer_lower:
            matched.append(kw)
        else:
            missing.append(kw)

    return {
        "pass": len(missing) == 0,
        "total": len(keywords),
        "matched": len(matched),
        "missing": missing,
    }


def check_must_not_contain(answer: str, keywords: list) -> dict:
    """Check if answer does NOT contain hallucination signals."""
    if not keywords:
        return {"pass": True, "found": []}

    answer_lower = answer.lower()
    found = [kw for kw in keywords if kw.lower() in answer_lower]

    return {
        "pass": len(found) == 0,
        "found": found,
    }


def check_expected_docs(related_docs: list, expected: list) -> dict:
    """Check if at least one expected doc appears in relatedDocs."""
    if not expected:
        return {"pass": True, "expected": expected, "found": []}

    found = []
    for doc in related_docs:
        doc_id = doc.get("docId", "").lower()
        for exp in expected:
            if exp.lower() in doc_id:
                found.append(exp)

    return {
        "pass": len(found) > 0,
        "expected": expected,
        "found": list(set(found)),
    }


def check_citation_present(sources: list, citations: list, chunks_retrieved: int = -1) -> dict:
    """Check if at least one source or citation is present.

    Not applicable when chunks_retrieved == 0 — the system correctly declines
    these queries and cannot cite nonexistent sources.
    """
    if chunks_retrieved == 0:
        return {
            "pass": True,
            "applicable": False,
            "source_count": 0,
            "citation_count": 0,
            "reason": "No chunks retrieved — citation N/A",
        }

    source_count = len(sources) if sources else 0
    citation_count = len(citations) if citations else 0

    return {
        "pass": source_count > 0 or citation_count > 0,
        "applicable": True,
        "source_count": source_count,
        "citation_count": citation_count,
    }


def check_oos_handling(answer: str, is_oos: bool, decline_signals: list) -> dict:
    """For OOS queries: check if at least one decline signal appears."""
    if not is_oos:
        return {"pass": True, "applicable": False, "signals_found": []}

    answer_lower = answer.lower()
    signals_found = [s for s in decline_signals if s.lower() in answer_lower]

    return {
        "pass": len(signals_found) > 0,
        "applicable": True,
        "signals_found": signals_found,
    }


def check_latency(latency_ms: int) -> dict:
    """Check if response time is under threshold."""
    return {
        "pass": latency_ms < LATENCY_THRESHOLD_MS,
        "latency_ms": latency_ms,
        "threshold_ms": LATENCY_THRESHOLD_MS,
    }


def run_checks(baseline: dict, result: dict) -> dict:
    """Run all 6 checks on a single query result."""
    if result["error"] or not result["response"]:
        # Return all-fail for errored queries
        return {
            "must_contain": {"pass": False, "total": 0, "matched": 0, "missing": []},
            "must_not_contain": {"pass": False, "found": ["(query failed)"]},
            "expected_docs": {"pass": False, "expected": baseline["expected_docs"], "found": []},
            "citation_present": {"pass": False, "applicable": True, "source_count": 0, "citation_count": 0},
            "oos_handling": {"pass": False, "applicable": baseline["is_oos"], "signals_found": []},
            "latency": {"pass": False, "latency_ms": result["latency_ms"], "threshold_ms": LATENCY_THRESHOLD_MS},
        }

    resp = result["response"]
    answer = resp.get("answer", "")
    sources = resp.get("sources", [])
    related_docs = resp.get("relatedDocs", [])
    citations = resp.get("citations", [])
    server_latency = resp.get("metadata", {}).get("latencyMs", result["latency_ms"])
    chunks_retrieved = resp.get("metadata", {}).get("chunksRetrieved", -1)

    return {
        "must_contain": check_must_contain(answer, baseline["must_contain"]),
        "must_not_contain": check_must_not_contain(answer, baseline["must_not_contain"]),
        "expected_docs": check_expected_docs(related_docs, baseline["expected_docs"]),
        "citation_present": check_citation_present(sources, citations, chunks_retrieved),
        "oos_handling": check_oos_handling(answer, baseline["is_oos"], baseline.get("oos_decline_signals", [])),
        "latency": check_latency(server_latency),
    }


# ---------------------------------------------------------------------------
# Step 4: Calculate Aggregate Metrics
# ---------------------------------------------------------------------------

def calculate_metrics(results: list) -> dict:
    """Calculate aggregate metrics from all query results."""
    successful = [r for r in results if r["error"] is None]
    in_scope = [r for r in successful if not r["is_oos"]]
    oos = [r for r in successful if r["is_oos"]]

    # Deflection rate: in-scope with all must_contain passing
    deflection_count = sum(1 for r in in_scope if r["checks"]["must_contain"]["pass"])
    deflection_rate = (deflection_count / len(in_scope) * 100) if in_scope else 0.0

    # Citation accuracy: in-scope with citation applicable and present
    citation_applicable = [r for r in in_scope if r["checks"]["citation_present"].get("applicable", True)]
    citation_count = sum(1 for r in citation_applicable if r["checks"]["citation_present"]["pass"])
    citation_accuracy = (citation_count / len(citation_applicable) * 100) if citation_applicable else 0.0
    # Also compute raw citation rate for transparency
    citation_count_raw = sum(1 for r in in_scope if r["checks"]["citation_present"]["pass"])
    citation_accuracy_raw = (citation_count_raw / len(in_scope) * 100) if in_scope else 0.0

    # Hallucination rate: any query with must_not_contain fail
    halluc_count = sum(1 for r in successful if not r["checks"]["must_not_contain"]["pass"])
    hallucination_rate = (halluc_count / len(successful) * 100) if successful else 0.0

    # OOS handling rate
    oos_pass = sum(1 for r in oos if r["checks"]["oos_handling"]["pass"])
    oos_handling_rate = (oos_pass / len(oos) * 100) if oos else 0.0

    # Latency
    latencies = [r["checks"]["latency"]["latency_ms"] for r in successful]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    latency_pass = sum(1 for l in latencies if l < LATENCY_THRESHOLD_MS)
    latency_pct = (latency_pass / len(latencies) * 100) if latencies else 0.0

    # Per-category breakdown
    categories = {}
    for cat in ["booking", "customs", "carrier", "sla", "edge_case"]:
        cat_results = [r for r in successful if r["category"] == cat]
        cat_inscope = [r for r in cat_results if not r["is_oos"]]
        cat_oos = [r for r in cat_results if r["is_oos"]]

        cat_defl = sum(1 for r in cat_inscope if r["checks"]["must_contain"]["pass"])
        cat_cite_applicable = [r for r in cat_inscope if r["checks"]["citation_present"].get("applicable", True)]
        cat_cite = sum(1 for r in cat_cite_applicable if r["checks"]["citation_present"]["pass"])
        cat_halluc = sum(1 for r in cat_results if not r["checks"]["must_not_contain"]["pass"])
        cat_latencies = [r["checks"]["latency"]["latency_ms"] for r in cat_results]

        categories[cat] = {
            "total": len(cat_results),
            "in_scope": len(cat_inscope),
            "oos": len(cat_oos),
            "citation_applicable": len(cat_cite_applicable),
            "deflection_rate": (cat_defl / len(cat_inscope) * 100) if cat_inscope else 0.0,
            "citation_accuracy": (cat_cite / len(cat_cite_applicable) * 100) if cat_cite_applicable else 0.0,
            "hallucination_rate": (cat_halluc / len(cat_results) * 100) if cat_results else 0.0,
            "avg_latency_ms": sum(cat_latencies) / len(cat_latencies) if cat_latencies else 0.0,
        }

    return {
        "deflection_rate": round(deflection_rate, 1),
        "citation_accuracy": round(citation_accuracy, 1),
        "citation_accuracy_raw": round(citation_accuracy_raw, 1),
        "citation_applicable_queries": len(citation_applicable),
        "citation_na_queries": len(in_scope) - len(citation_applicable),
        "hallucination_rate": round(hallucination_rate, 1),
        "oos_handling_rate": round(oos_handling_rate, 1),
        "avg_latency_ms": round(avg_latency, 0),
        "latency_under_5s": round(latency_pct, 1),
        "total_queries": len(results),
        "successful_queries": len(successful),
        "failed_queries": len(results) - len(successful),
        "in_scope_queries": len(in_scope),
        "oos_queries": len(oos),
        "by_category": categories,
    }


# ---------------------------------------------------------------------------
# Step 5: Generate Output Files
# ---------------------------------------------------------------------------

def write_results_json(results: list, metrics: dict, config: dict):
    """Write data/evaluation_results.json."""
    RESULTS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)

    run_id = f"eval-{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}"

    output = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": config,
        "metrics": metrics,
        "results": results,
    }

    with open(RESULTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)

    print(f"  JSON: {RESULTS_JSON_PATH}")
    return run_id


def write_results_csv(results: list):
    """Write data/evaluation_results.csv."""
    RESULTS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "id", "category", "query", "is_oos", "confidence",
        "must_contain_pass", "must_contain_matched", "must_contain_total",
        "must_not_contain_pass", "expected_docs_pass", "citation_present",
        "citation_applicable",
        "oos_handling_pass", "latency_ms", "overall_pass", "error",
    ]

    with open(RESULTS_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for r in results:
            confidence = ""
            if r["response"]:
                confidence = r["response"].get("confidence", {}).get("level", "")

            writer.writerow({
                "id": r["id"],
                "category": r["category"],
                "query": r["query"],
                "is_oos": r["is_oos"],
                "confidence": confidence,
                "must_contain_pass": r["checks"]["must_contain"]["pass"],
                "must_contain_matched": r["checks"]["must_contain"]["matched"],
                "must_contain_total": r["checks"]["must_contain"]["total"],
                "must_not_contain_pass": r["checks"]["must_not_contain"]["pass"],
                "expected_docs_pass": r["checks"]["expected_docs"]["pass"],
                "citation_present": r["checks"]["citation_present"]["pass"],
                "citation_applicable": r["checks"]["citation_present"].get("applicable", True),
                "oos_handling_pass": r["checks"]["oos_handling"]["pass"],
                "latency_ms": r["checks"]["latency"]["latency_ms"],
                "overall_pass": r["overall_pass"],
                "error": r["error"] or "",
            })

    print(f"  CSV:  {RESULTS_CSV_PATH}")


def write_report_md(results: list, metrics: dict, run_id: str):
    """Write reports/evaluation_report.md."""
    REPORT_MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    def status(value, target, higher_is_better=True):
        if higher_is_better:
            return "PASS" if value >= target else "FAIL"
        else:
            return "PASS" if value < target else "FAIL"

    lines = []
    lines.append("# Evaluation Report")
    lines.append("")
    lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Run ID**: {run_id}")
    lines.append(f"**Queries**: {metrics['total_queries']} ({metrics['in_scope_queries']} in-scope, {metrics['oos_queries']} OOS)")
    lines.append(f"**Successful**: {metrics['successful_queries']} / {metrics['total_queries']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Aggregate metrics
    lines.append("## Aggregate Metrics")
    lines.append("")
    lines.append("| Metric | Result | Target | Status |")
    lines.append("|--------|--------|--------|--------|")
    lines.append(f"| Deflection Rate | {metrics['deflection_rate']}% | >= {TARGETS['deflection_rate']}% | {status(metrics['deflection_rate'], TARGETS['deflection_rate'])} |")
    lines.append(f"| Citation Accuracy | {metrics['citation_accuracy']}% | >= {TARGETS['citation_accuracy']}% | {status(metrics['citation_accuracy'], TARGETS['citation_accuracy'])} |")
    if metrics.get("citation_na_queries", 0) > 0:
        lines.append(f"| Citation (raw) | {metrics['citation_accuracy_raw']}% | - | (includes {metrics['citation_na_queries']} N/A queries) |")
    lines.append(f"| Hallucination Rate | {metrics['hallucination_rate']}% | < {TARGETS['hallucination_rate']}% | {status(metrics['hallucination_rate'], TARGETS['hallucination_rate'], higher_is_better=False)} |")
    lines.append(f"| OOS Handling | {metrics['oos_handling_rate']}% | >= {TARGETS['oos_handling_rate']}% | {status(metrics['oos_handling_rate'], TARGETS['oos_handling_rate'])} |")
    lines.append(f"| Avg Latency | {metrics['avg_latency_ms']}ms | < {TARGETS['avg_latency_ms']}ms | {status(metrics['avg_latency_ms'], TARGETS['avg_latency_ms'], higher_is_better=False)} |")
    lines.append(f"| Latency < 5s | {metrics['latency_under_5s']}% | - | - |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-category breakdown
    lines.append("## Per-Category Breakdown")
    lines.append("")
    lines.append("| Category | Queries | Deflection | Citation | Hallucination | Avg Latency |")
    lines.append("|----------|---------|------------|----------|--------------|-------------|")
    for cat in ["booking", "customs", "carrier", "sla", "edge_case"]:
        c = metrics["by_category"][cat]
        lines.append(f"| {cat} | {c['total']} | {c['deflection_rate']:.1f}% | {c['citation_accuracy']:.1f}% | {c['hallucination_rate']:.1f}% | {c['avg_latency_ms']:.0f}ms |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Failures: must_contain
    mc_fails = [r for r in results if r["error"] is None and not r["checks"]["must_contain"]["pass"] and not r["is_oos"]]
    if mc_fails:
        lines.append("## must_contain Failures")
        lines.append("")
        lines.append("| Query | Missing Keywords |")
        lines.append("|-------|-----------------|")
        for r in mc_fails:
            missing = ", ".join(r["checks"]["must_contain"]["missing"])
            lines.append(f"| {r['id']} | {missing} |")
        lines.append("")

    # Failures: hallucination
    halluc_fails = [r for r in results if r["error"] is None and not r["checks"]["must_not_contain"]["pass"]]
    if halluc_fails:
        lines.append("## Hallucination Detections")
        lines.append("")
        lines.append("| Query | Found Signals |")
        lines.append("|-------|--------------|")
        for r in halluc_fails:
            found = ", ".join(r["checks"]["must_not_contain"]["found"])
            lines.append(f"| {r['id']} | {found} |")
        lines.append("")

    # Failures: OOS
    oos_fails = [r for r in results if r["error"] is None and r["is_oos"] and not r["checks"]["oos_handling"]["pass"]]
    if oos_fails:
        lines.append("## OOS Handling Failures")
        lines.append("")
        lines.append("| Query | Answer Excerpt |")
        lines.append("|-------|---------------|")
        for r in oos_fails:
            answer = r["response"].get("answer", "")[:100] if r["response"] else "(no response)"
            lines.append(f"| {r['id']} | {answer} |")
        lines.append("")

    # Citation N/A: 0-chunk queries where citation is not applicable
    cite_na = [r for r in results if r["error"] is None and not r["is_oos"]
               and not r["checks"]["citation_present"].get("applicable", True)]
    if cite_na:
        lines.append("## Citation N/A (0 chunks — correct decline)")
        lines.append("")
        lines.append("| Query | Confidence | Reason |")
        lines.append("|-------|-----------|--------|")
        for r in cite_na:
            conf = r["response"].get("confidence", {}).get("level", "?") if r["response"] else "?"
            reason = r["checks"]["citation_present"].get("reason", "N/A")
            lines.append(f"| {r['id']} | {conf} | {reason} |")
        lines.append("")

    # Failures: citation (genuine — has chunks but no citation)
    cite_fails = [r for r in results if r["error"] is None and not r["is_oos"]
                  and r["checks"]["citation_present"].get("applicable", True)
                  and not r["checks"]["citation_present"]["pass"]]
    if cite_fails:
        lines.append("## Citation Missing (In-Scope, Chunks Available)")
        lines.append("")
        lines.append("| Query | Confidence |")
        lines.append("|-------|-----------|")
        for r in cite_fails:
            conf = r["response"].get("confidence", {}).get("level", "?") if r["response"] else "?"
            lines.append(f"| {r['id']} | {conf} |")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Raw query results table
    lines.append("## Raw Query Results")
    lines.append("")
    lines.append("| ID | Category | Confidence | Deflect | Citation | Halluc | OOS | Latency | Pass |")
    lines.append("|----|----------|------------|---------|----------|--------|-----|---------|------|")
    for r in results:
        if r["error"]:
            lines.append(f"| {r['id']} | {r['category']} | ERROR | - | - | - | - | - | FAIL |")
            continue

        conf = r["response"].get("confidence", {}).get("level", "?") if r["response"] else "?"
        mc = "PASS" if r["checks"]["must_contain"]["pass"] else "FAIL"
        cite_check = r["checks"]["citation_present"]
        if not cite_check.get("applicable", True):
            cite = "N/A"
        else:
            cite = "PASS" if cite_check["pass"] else "FAIL"
        halluc = "PASS" if r["checks"]["must_not_contain"]["pass"] else "FAIL"
        oos_str = "PASS" if r["checks"]["oos_handling"]["pass"] else "FAIL"
        if not r["checks"]["oos_handling"].get("applicable", True):
            oos_str = "-"
        lat = f"{r['checks']['latency']['latency_ms']}ms"
        overall = "PASS" if r["overall_pass"] else "FAIL"

        lines.append(f"| {r['id']} | {r['category']} | {conf} | {mc} | {cite} | {halluc} | {oos_str} | {lat} | {overall} |")

    lines.append("")

    with open(REPORT_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Report: {REPORT_MD_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Waypoint Co-Pilot Evaluation Harness")
    parser.add_argument("--delay", type=int, default=DEFAULT_DELAY,
                        help=f"Seconds between API calls (default: {DEFAULT_DELAY})")
    parser.add_argument("--start-from", type=str, default="Q-01",
                        help="Resume from a specific query ID (e.g., Q-15)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Load baselines and validate, don't send queries")
    parser.add_argument("--api-url", type=str, default=DEFAULT_API_URL,
                        help=f"API base URL (default: {DEFAULT_API_URL})")
    args = parser.parse_args()

    print("=" * 60)
    print("  Waypoint Co-Pilot - Evaluation Harness")
    print("=" * 60)
    print(f"  API:    {args.api_url}")
    print(f"  Delay:  {args.delay}s between queries")
    print(f"  Start:  {args.start_from}")
    print(f"  Mode:   {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()

    # Load baselines
    baselines = load_baselines()
    in_scope = sum(1 for q in baselines if not q["is_oos"])
    oos = sum(1 for q in baselines if q["is_oos"])
    print(f"  {in_scope} in-scope, {oos} out-of-scope")

    if args.dry_run:
        print("\n--- DRY RUN: Validating baselines ---")
        mc_total = sum(len(q["must_contain"]) for q in baselines)
        mnc_total = sum(len(q["must_not_contain"]) for q in baselines)
        sc_total = sum(len(q["should_contain"]) for q in baselines)
        print(f"  must_contain keywords:     {mc_total}")
        print(f"  should_contain keywords:   {sc_total}")
        print(f"  must_not_contain keywords: {mnc_total}")

        # Validate all in-scope have >= 2 must_contain
        mc_low = [q["id"] for q in baselines if not q["is_oos"] and len(q["must_contain"]) < 2]
        if mc_low:
            print(f"  WARNING: In-scope with <2 must_contain: {mc_low}")
        else:
            print(f"  All in-scope queries have >= 2 must_contain PASS")

        # Validate all OOS have decline signals
        oos_no_sig = [q["id"] for q in baselines if q["is_oos"] and len(q.get("oos_decline_signals", [])) < 1]
        if oos_no_sig:
            print(f"  WARNING: OOS with no decline signals: {oos_no_sig}")
        else:
            print(f"  All OOS queries have >= 1 decline signal PASS")

        est_time = len(baselines) * args.delay
        print(f"\n  Estimated run time: {est_time // 60}m {est_time % 60}s (at {args.delay}s delay)")
        print("\nDry run complete. Use without --dry-run to execute.")
        return

    # Live run
    est_time = len(baselines) * args.delay
    print(f"\n  Estimated run time: ~{est_time // 60}m {est_time % 60}s")
    print(f"\nSending queries...\n")

    try:
        results = run_all_queries(baselines, args.api_url, args.delay, args.start_from)
    except KeyboardInterrupt:
        print(f"\n\nInterrupted! Saving {len(results) if 'results' in dir() else 0} partial results...")
        results = results if 'results' in dir() else []

    if not results:
        print("\nNo results to report.")
        return

    # Calculate metrics
    metrics = calculate_metrics(results)

    # Write outputs
    print(f"\nWriting output files...")
    config_info = {
        "delay_seconds": args.delay,
        "api_url": args.api_url,
        "start_from": args.start_from,
        "baselines_version": "1.0",
    }
    run_id = write_results_json(results, metrics, config_info)
    write_results_csv(results)
    write_report_md(results, metrics, run_id)

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"  EVALUATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Queries:         {metrics['successful_queries']}/{metrics['total_queries']} successful")
    print(f"  Deflection Rate: {metrics['deflection_rate']}% (target: >= {TARGETS['deflection_rate']}%)")
    print(f"  Citation Acc:    {metrics['citation_accuracy']}% (target: >= {TARGETS['citation_accuracy']}%)")
    print(f"  Hallucination:   {metrics['hallucination_rate']}% (target: < {TARGETS['hallucination_rate']}%)")
    print(f"  OOS Handling:    {metrics['oos_handling_rate']}% (target: >= {TARGETS['oos_handling_rate']}%)")
    print(f"  Avg Latency:     {metrics['avg_latency_ms']}ms (target: < {TARGETS['avg_latency_ms']}ms)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
