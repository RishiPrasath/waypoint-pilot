# Command Conventions

These conventions apply to every task in this sequence.

## PowerShell and Git

- Run one command per PowerShell block. Do not paste concatenated commands.
- Define and verify `$RepoRoot`, `$WorktreeRoot`, `$Branch`, and
  `$WorktreePath` before worktree operations.
- Use a short worktree path such as `C:\tmp\rag-bt001-fastapi-skeleton`.
- Before adding a worktree, fetch `origin` and enable long paths:

```powershell
git -C $RepoRoot fetch origin
git -C $RepoRoot config core.longpaths true
git -C $RepoRoot config --get core.longpaths
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

- If checkout fails after the branch is created, reuse the existing branch with
  `git worktree add $WorktreePath $Branch`; do not run `-b` again.
- Before cleanup, change the terminal directory outside the worktree. Remove
  only the verified task worktree, then prune and inspect the list.

## File writes

Windows PowerShell `Set-Content -Encoding UTF8` can introduce a BOM that breaks
some tools. For UTF-8 files, use a BOM-free write:

```powershell
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
```

Existing task files may contain older `Set-Content -Encoding UTF8` examples.
Those examples are non-authoritative and must be replaced by the BOM-free
helper above before execution. In PowerShell 7+, `Set-Content -Encoding
utf8NoBOM` is also acceptable; Windows PowerShell 5.1 should use the helper.

Keep separate commands separate; a missing newline can merge two commands into a
single malformed command.

## Python and tests

- Run the service tests from `pilot_phase2_poc/rag-service`.
- Use `uv run python -m pytest -q` so the module root is on `sys.path`.
- If a console-script invocation is required, configure the project explicitly
  with `pythonpath = ["."]` and record why.
- Record interpreter, dependency, test, and static-check results in evidence.

## Directories and cleanup

Git does not track empty directories. Add a purposeful `.gitkeep` or README when
an empty directory is part of the required structure. Never remove a worktree
while a terminal or IDE is currently inside it.
