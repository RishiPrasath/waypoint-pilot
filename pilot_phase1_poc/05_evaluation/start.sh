#!/usr/bin/env bash
# Waypoint Pilot - Startup Script (Bash)
# Starts the Node.js backend (port 3000) and React frontend (port 5173)

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
PIDS=()

cleanup() {
    echo ""
    echo "Shutting down..."
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            wait "$pid" 2>/dev/null
        fi
    done
    echo "Done."
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

echo ""
echo "=== Waypoint Pilot ==="
echo ""

# --- Pre-flight checks ---

# 1. Node.js
if ! command -v node &>/dev/null; then
    echo "[ERROR] Node.js not found. Install from https://nodejs.org"
    exit 1
fi

# 2. Python venv
if [ -f "$ROOT/venv/bin/python" ]; then
    PYTHON_EXE="$ROOT/venv/bin/python"
elif [ -f "$ROOT/venv/Scripts/python.exe" ]; then
    PYTHON_EXE="$ROOT/venv/Scripts/python.exe"
else
    echo "[ERROR] Python venv not found."
    echo "  Run: python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# 3. Backend node_modules
if [ ! -d "$ROOT/node_modules" ]; then
    echo "[SETUP] Installing backend dependencies..."
    (cd "$ROOT" && npm install)
fi

# 4. Client node_modules
if [ ! -d "$ROOT/client/node_modules" ]; then
    echo "[SETUP] Installing frontend dependencies..."
    (cd "$ROOT/client" && npm install)
fi

# 5. ChromaDB
if [ ! -d "$ROOT/chroma_db" ]; then
    echo "[WARN] chroma_db/ not found. Run ingestion first:"
    echo "  $PYTHON_EXE scripts/ingest.py"
fi

# --- Start services ---

echo "[1/2] Starting backend on http://localhost:3000 ..."
(cd "$ROOT" && node backend/index.js) &
PIDS+=($!)

echo "[2/2] Starting frontend on http://localhost:5173 ..."
(cd "$ROOT/client" && npx vite --host) &
PIDS+=($!)

echo ""
echo "=== Services Running ==="
echo "  Backend  : http://localhost:3000/api/health"
echo "  Frontend : http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services."
echo ""

# Wait for any child to exit
wait -n 2>/dev/null || wait
