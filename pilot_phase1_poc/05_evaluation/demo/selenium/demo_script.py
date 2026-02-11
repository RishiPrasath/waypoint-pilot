"""
Waypoint POC Demo — Selenium Screenshot Capture Script

Runs 10 demo queries through the React UI and captures screenshots
at two states per query: "typed" (before submit) and "response" (after render).

Prerequisites:
  - Backend running: cd pilot_phase1_poc/05_evaluation && npm start
  - Frontend running: cd pilot_phase1_poc/05_evaluation/client && npm run dev
  - Selenium installed: pip install -r requirements.txt

Usage:
  python demo_script.py              # Run all 10 queries
  python demo_script.py --quick      # Run first 2 queries only (smoke test)
  python demo_script.py --headless   # Run headless (no visible browser)
"""

import argparse
import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# ── Demo Queries (from Task 5.1) ──────────────────────────────────────────

DEMO_QUERIES = [
    {"num": 1,  "id": "Q-01", "query": "What documents are needed for sea freight Singapore to Indonesia?", "type": "happy"},
    {"num": 2,  "id": "Q-11", "query": "What's the GST rate for imports into Singapore?", "type": "happy"},
    {"num": 3,  "id": "Q-13", "query": "Is Certificate of Origin required for Thailand?", "type": "happy"},
    {"num": 4,  "id": "Q-24", "query": "How do I submit VGM to Maersk?", "type": "happy"},
    {"num": 5,  "id": "Q-14", "query": "What permits are needed to import cosmetics to Indonesia?", "type": "happy"},
    {"num": 6,  "id": "Q-03", "query": "What's the difference between FCL and LCL?", "type": "happy"},
    {"num": 7,  "id": "Q-31", "query": "What's our standard delivery SLA for Singapore?", "type": "happy"},
    {"num": 8,  "id": "Q-42", "query": "Where is my shipment right now?", "type": "oos"},
    {"num": 9,  "id": "Q-46", "query": "What's the weather forecast for shipping?", "type": "oos"},
    {"num": 10, "id": "Q-04", "query": "When is the SI cutoff for this week's Maersk sailing?", "type": "boundary"},
]

# ── Configuration ──────────────────────────────────────────────────────────

FRONTEND_URL = "http://localhost:5173"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
RESPONSE_TIMEOUT = 15       # seconds to wait for API response
BETWEEN_QUERY_PAUSE = 2     # seconds between queries

# Paths (relative to this script's location)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent.parent   # 05_evaluation/
SCREENSHOT_DIR = SCRIPT_DIR.parent / "presentation" / "public" / "demo" / "screenshots"
RESULTS_FILE = SCRIPT_DIR / "demo_results.txt"


def create_driver(headless=False):
    """Create and configure Chrome WebDriver."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    # Suppress DevTools noise
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    return driver


def wait_for_page_load(driver):
    """Wait for the Waypoint UI to fully load."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Waypoint Co-Pilot')]"))
    )
    # Extra beat for React hydration
    time.sleep(0.5)


def clear_previous_state(driver):
    """Clear any existing query text and response from the UI."""
    try:
        input_el = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search query"]')
        # Select all and delete to clear
        input_el.send_keys(Keys.CONTROL, "a")
        input_el.send_keys(Keys.DELETE)
        time.sleep(0.3)
    except Exception:
        pass

    # Wait for any response card to disappear (if present from previous query)
    try:
        WebDriverWait(driver, 2).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "div.rounded-xl.border.shadow-sm.overflow-hidden")
            )
        )
    except Exception:
        # No response card visible — that's fine
        pass


def type_query(driver, query_text):
    """Type a query into the search input."""
    input_el = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[aria-label="Search query"]'))
    )
    input_el.clear()
    input_el.send_keys(query_text)
    time.sleep(0.3)  # Let React update the controlled input


def submit_query(driver):
    """Click the Search button to submit the query."""
    btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    btn.click()


def wait_for_response(driver):
    """Wait for loading to finish and a response to appear. Returns elapsed seconds."""
    start = time.time()

    # Wait for loading indicator to disappear
    try:
        WebDriverWait(driver, RESPONSE_TIMEOUT).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Searching knowledge base')]")
            )
        )
    except Exception:
        pass

    # Wait for either: response card OR a text paragraph in main content
    try:
        WebDriverWait(driver, 5).until(
            lambda d: (
                d.find_elements(By.CSS_SELECTOR, "div.rounded-xl.border.shadow-sm.overflow-hidden")
                or d.find_elements(By.CSS_SELECTOR, "div.bg-rose-50")
            )
        )
    except Exception:
        pass

    # Small buffer for animations/rendering to complete
    time.sleep(0.5)
    return time.time() - start


def check_page_scrolls(driver):
    """Check if the page content extends beyond the viewport."""
    body_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    return body_height > viewport_height + 50  # 50px buffer


def capture_screenshot(driver, filepath):
    """Save a screenshot to the given path."""
    driver.save_screenshot(str(filepath))


def capture_full_page_screenshot(driver, filepath):
    """Capture a full-page screenshot by temporarily resizing the window."""
    original_size = driver.get_window_size()
    body_height = driver.execute_script("return document.body.scrollHeight")

    # Resize to full page height
    driver.set_window_size(WINDOW_WIDTH, body_height + 100)
    time.sleep(0.3)
    driver.save_screenshot(str(filepath))

    # Restore original size
    driver.set_window_size(original_size["width"], original_size["height"])
    time.sleep(0.2)


def run_demo(queries, headless=False):
    """Run the full demo sequence, capturing screenshots for each query."""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Waypoint POC Demo — Screenshot Capture")
    print(f"  Queries: {len(queries)} | Resolution: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    print(f"  Output:  {SCREENSHOT_DIR}")
    print(f"{'='*60}\n")

    driver = create_driver(headless=headless)
    results = []

    try:
        # Navigate to frontend
        print(f"  Navigating to {FRONTEND_URL}...")
        driver.get(FRONTEND_URL)
        wait_for_page_load(driver)
        print(f"  Page loaded successfully.\n")

        for i, q in enumerate(queries):
            num = q["num"]
            qid = q["id"]
            query_text = q["query"]
            qtype = q["type"]
            prefix = f"[{i+1}/{len(queries)}] Demo {num} ({qid})"

            print(f"  {prefix}: {query_text[:60]}...")

            try:
                # Step 1: Clear previous state
                if i > 0:
                    clear_previous_state(driver)

                # Step 2: Type query
                print(f"    Typing query...")
                type_query(driver, query_text)

                # Step 3: Screenshot — typed state
                typed_path = SCREENSHOT_DIR / f"demo_{num:02d}_typed.png"
                capture_screenshot(driver, typed_path)
                print(f"    Captured: {typed_path.name}")

                # Step 4: Submit
                print(f"    Submitting...")
                submit_query(driver)

                # Step 5: Wait for response
                elapsed = wait_for_response(driver)

                # Step 6: Screenshot — response state
                response_path = SCREENSHOT_DIR / f"demo_{num:02d}_response.png"
                capture_screenshot(driver, response_path)
                print(f"    Captured: {response_path.name} ({elapsed:.1f}s)")

                # Step 7: Full-page screenshot if content scrolls
                if check_page_scrolls(driver):
                    full_path = SCREENSHOT_DIR / f"demo_{num:02d}_response_full.png"
                    capture_full_page_screenshot(driver, full_path)
                    print(f"    Captured: {full_path.name} (full-page)")

                results.append({
                    "num": num, "id": qid, "query": query_text,
                    "type": qtype, "status": "OK", "elapsed": elapsed,
                })
                print(f"    Done.\n")

            except Exception as e:
                error_msg = str(e)[:100]
                print(f"    ERROR: {error_msg}")

                # Capture error state screenshot
                try:
                    error_path = SCREENSHOT_DIR / f"demo_{num:02d}_error.png"
                    capture_screenshot(driver, error_path)
                    print(f"    Captured: {error_path.name} (error state)")
                except Exception:
                    pass

                results.append({
                    "num": num, "id": qid, "query": query_text,
                    "type": qtype, "status": f"ERROR: {error_msg}", "elapsed": 0,
                })
                print()

            # Pause between queries
            if i < len(queries) - 1:
                time.sleep(BETWEEN_QUERY_PAUSE)

    finally:
        driver.quit()

    # ── Summary ────────────────────────────────────────────────────────────
    succeeded = [r for r in results if r["status"] == "OK"]
    failed = [r for r in results if r["status"] != "OK"]
    avg_elapsed = sum(r["elapsed"] for r in succeeded) / len(succeeded) if succeeded else 0

    summary_lines = [
        "Waypoint POC Demo — Results Summary",
        "=" * 40,
        f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Queries run: {len(results)}",
        f"Succeeded: {len(succeeded)}",
        f"Failed: {len(failed)}",
        f"Avg response time: {avg_elapsed:.1f}s",
        "",
        "Per-query results:",
        "-" * 40,
    ]
    for r in results:
        status = "OK" if r["status"] == "OK" else "FAIL"
        elapsed_str = f"{r['elapsed']:.1f}s" if r["elapsed"] > 0 else "N/A"
        summary_lines.append(
            f"  Demo {r['num']:2d} ({r['id']}) [{r['type']:8s}] — {status:4s} ({elapsed_str})"
        )

    if failed:
        summary_lines.append("")
        summary_lines.append("Failures:")
        for r in failed:
            summary_lines.append(f"  Demo {r['num']}: {r['status']}")

    summary_lines.append("")
    summary_lines.append(f"Screenshots saved to: {SCREENSHOT_DIR}")
    summary_text = "\n".join(summary_lines)

    print(f"\n{'='*60}")
    print(summary_text)
    print(f"{'='*60}\n")

    # Save summary to file
    RESULTS_FILE.write_text(summary_text, encoding="utf-8")
    print(f"  Summary saved to: {RESULTS_FILE}\n")

    return len(failed) == 0


def main():
    parser = argparse.ArgumentParser(description="Waypoint POC Demo Screenshot Capture")
    parser.add_argument("--quick", action="store_true", help="Run only first 2 queries (smoke test)")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")
    args = parser.parse_args()

    queries = DEMO_QUERIES[:2] if args.quick else DEMO_QUERIES

    success = run_demo(queries, headless=args.headless)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
