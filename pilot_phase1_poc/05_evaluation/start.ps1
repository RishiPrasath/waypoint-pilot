# Waypoint Pilot - Startup Script (PowerShell)
# Starts the Node.js backend (port 3000) and React frontend (port 5173)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot

Write-Host ""
Write-Host "=== Waypoint Pilot ===" -ForegroundColor Cyan
Write-Host ""

# --- Pre-flight checks ---

# 1. Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Node.js not found. Install from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# 2. Python venv
$PythonExe = Join-Path $Root "venv\Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "[ERROR] Python venv not found at venv\Scripts\python.exe" -ForegroundColor Red
    Write-Host "  Run: py -3.11 -m venv venv && venv\Scripts\activate && pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# 3. Backend node_modules
if (-not (Test-Path (Join-Path $Root "node_modules"))) {
    Write-Host "[SETUP] Installing backend dependencies..." -ForegroundColor Yellow
    Push-Location $Root
    npm install
    Pop-Location
}

# 4. Client node_modules
$ClientDir = Join-Path $Root "client"
if (-not (Test-Path (Join-Path $ClientDir "node_modules"))) {
    Write-Host "[SETUP] Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location $ClientDir
    npm install
    Pop-Location
}

# 5. ChromaDB
if (-not (Test-Path (Join-Path $Root "chroma_db"))) {
    Write-Host "[WARN] chroma_db/ not found. Run ingestion first:" -ForegroundColor Yellow
    Write-Host "  venv\Scripts\python.exe scripts\ingest.py" -ForegroundColor Yellow
}

# --- Free ports if occupied ---
foreach ($port in @(3000, 5173)) {
    $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        $procId = $conn[0].OwningProcess
        Write-Host "[CLEANUP] Port $port in use by PID $procId - stopping it." -ForegroundColor Yellow
        Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
    }
}

# --- Start services ---

Write-Host "[1/2] Starting backend on http://localhost:3000 ..." -ForegroundColor Green
$backend = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c node backend/index.js" `
    -WorkingDirectory $Root `
    -PassThru -NoNewWindow

Write-Host "[2/2] Starting frontend on http://localhost:5173 ..." -ForegroundColor Green
$frontend = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c npx vite --host" `
    -WorkingDirectory $ClientDir `
    -PassThru -NoNewWindow

Write-Host ""
Write-Host "=== Services Running ===" -ForegroundColor Cyan
Write-Host "  Backend  : http://localhost:3000/api/health" -ForegroundColor White
Write-Host "  Frontend : http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop all services." -ForegroundColor DarkGray
Write-Host ""

# --- Graceful shutdown ---
try {
    while (-not $backend.HasExited -and -not $frontend.HasExited) {
        Start-Sleep -Milliseconds 500
    }
}
finally {
    Write-Host ""
    Write-Host "Shutting down..." -ForegroundColor Yellow

    # Kill process trees (cmd.exe children include node/npx)
    foreach ($entry in @(@{Name="Backend"; Proc=$backend}, @{Name="Frontend"; Proc=$frontend})) {
        $p = $entry.Proc
        if ($p -and -not $p.HasExited) {
            Get-CimInstance Win32_Process |
                Where-Object { $_.ParentProcessId -eq $p.Id } |
                ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
            Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
            Write-Host ("  " + $entry.Name + " stopped.") -ForegroundColor DarkGray
        }
    }

    Write-Host "Done." -ForegroundColor Green
}
