# Command Conventions

Run commands one at a time. Do not paste multiple Git commands onto one
PowerShell line.

Use a short worktree root by default:

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
```

Refresh `main` before creating a task branch:

```powershell
git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot config core.longpaths true
```

Use the Python module form for tests:

```powershell
uv run python -m pytest -q
```

For BOM-sensitive files, use the .NET UTF-8-no-BOM writer rather than
`Set-Content -Encoding UTF8`:

```powershell
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
```
