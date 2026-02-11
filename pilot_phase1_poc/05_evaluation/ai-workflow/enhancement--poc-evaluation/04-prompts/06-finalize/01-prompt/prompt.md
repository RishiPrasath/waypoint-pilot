# Phase 6 — Buffer, Polish & Finalize (Tasks 6.1 + 6.2 + 6.3)

## Persona
DevOps engineer running final validation, creating the release commit, and updating project-level documentation to mark Week 4 complete.

## Context

### Workspace
- **Root**: `pilot_phase1_poc/05_evaluation/`
- **Backend**: Express API on port 3000 (`npm start`)
- **Frontend**: React Vite on port 5173 (`cd client && npm run dev`)
- **Presentation**: Vite on port 5174 (`cd demo/presentation && npm run dev`)
- **Python venv**: `venv/Scripts/activate` (Windows)

### Current State
- **42/45 tasks complete (93%)** — Phases 0–5 all done
- **All 6 evaluation targets met** in Round 4
- Presentation app: 14 slides, 3 Mermaid diagrams, Framer Motion animations
- Q&A doc: 20 anticipated questions with data-backed answers
- 25 demo screenshots in `demo/presentation/public/demo/screenshots/`

### .gitignore Coverage (root)
Already excludes: `venv/`, `node_modules/`, `chroma_db/`, `.env`, `__pycache__/`, `.pytest_cache/`, `dist/`, `build/`, `logs/*.log`, `.vscode/`, `.idea/`

### Demo Queries (for smoke test)
10 queries from `demo/demo_queries.md`:
1. Q-01: "What documents are needed for sea freight Singapore to Indonesia?"
2. Q-11: "What's the GST rate for imports into Singapore?"
3. Q-13: "What are the customs clearance procedures for importing goods into Singapore?"
4. Q-24: "What are the VGM requirements for Maersk shipments?"
5. Q-14: "What documentation is needed for importing controlled goods?"
6. Q-03: "What are the Incoterms 2020 rules for sea freight?"
7. Q-31: "What is the company's SLA for responding to customer queries?"
8. Q-42: "Can you track my shipment BK-2024-1234?"
9. Q-46: "What's the current freight rate from Singapore to Rotterdam?"
10. Q-04: "How do I apply for a customs permit in Singapore?"

---

## Task

Execute all 3 Phase 6 tasks sequentially.

### Task 6.1 — Final Smoke Test

**Objective**: Confirm the entire system works from cold start.

**Steps**:

1. **Kill any stale processes** on ports 3000, 5173, 5174:
   ```bash
   netstat -ano | findstr :3000
   netstat -ano | findstr :5173
   netstat -ano | findstr :5174
   # Kill any found: cmd //c "taskkill /PID N /F"
   ```

2. **Cold-start backend**:
   ```bash
   cd pilot_phase1_poc/05_evaluation
   npm start
   ```
   Verify: `GET http://localhost:3000/api/health` returns JSON with status "ok"

3. **Cold-start frontend**:
   ```bash
   cd pilot_phase1_poc/05_evaluation/client
   npm run dev
   ```
   Verify: `http://localhost:5173` loads the Waypoint Co-Pilot UI

4. **Run 3 representative demo queries** (1 happy, 1 OOS, 1 boundary) via the UI or API:
   - Happy: Q-11 "What's the GST rate for imports into Singapore?"
   - OOS: Q-42 "Can you track my shipment BK-2024-1234?"
   - Boundary: Q-04 "How do I apply for a customs permit in Singapore?"

   For each, verify:
   - Response renders with all 4 sections (Answer, Sources, Related Docs, Confidence)
   - No console errors
   - Latency < 5 seconds

5. **Test error handling**:
   - Submit empty query → should show validation message or empty state
   - Submit very long query (500+ chars) → should still respond

6. **Verify presentation app**:
   ```bash
   cd pilot_phase1_poc/05_evaluation/demo/presentation
   npm run dev
   ```
   - Navigate to first and last slide (Slide 1 title, Slide 14 Q&A)
   - Verify at least 1 Mermaid diagram renders (Slide 5 or 6)
   - Verify demo carousel loads screenshots (Slide 9)

7. **Document results** in the output report (pass/fail per check)

### Task 6.2 — Backup (Git Commit)

**Objective**: Create a git commit capturing all Week 4 work.

**Steps**:

1. Run `git status` to review all changes
2. Verify no sensitive files staged:
   - No `.env` files with API keys
   - No `chroma_db/` directories
   - No `node_modules/` directories
   - No `venv/` directories
3. Check `.gitignore` covers all transient artifacts (already confirmed: root `.gitignore` is comprehensive)
4. Stage all relevant Week 4 files:
   ```bash
   git add pilot_phase1_poc/05_evaluation/
   git add CLAUDE.md AGENTS.md
   ```
5. Create commit with descriptive message covering Phase 5 (Demo) and Phase 6 (Finalize):
   ```
   Complete Phase 5 Demo + Phase 6 Finalize: presentation app, Q&A, smoke test (42/45, 93%)
   ```
6. Run `git status` to confirm clean state

**IMPORTANT**: Do NOT push to remote. Only create a local commit.

### Task 6.3 — Update CLAUDE.md (Week 4 Complete)

**Objective**: Mark Week 4 as complete in root CLAUDE.md and update Active Initiatives.

**Steps**:

1. Update the **Active Initiatives** table in `CLAUDE.md`:
   - Change Week 4 status from `🔄 In Progress (42/45 — 93%)` to `✅ Complete (45/45 — 100%)`

2. Also update in `AGENTS.md` and `ai-workflow-bootstrap-prompt-v3.md`

3. Update the `MEMORY.md` auto memory file:
   - Update "Current State" to reflect Week 4 complete
   - Add any final lessons learned

4. Create output report for Phase 6

---

## Format

### Validation Checklist

**Task 6.1 — Smoke Test**:
- [ ] System starts from cold without errors (backend + frontend)
- [ ] Health endpoint returns OK
- [ ] Happy path query returns response with 4 sections
- [ ] OOS query returns graceful decline
- [ ] Boundary query returns response with citations
- [ ] All queries < 5s latency
- [ ] Error handling works (empty query)
- [ ] Presentation app renders (Slide 1, Slide 14, 1 Mermaid diagram, carousel)
- [ ] No console errors

**Task 6.2 — Git Commit**:
- [ ] No sensitive files in commit
- [ ] All Week 4 files staged
- [ ] Commit message is descriptive
- [ ] Repository in clean state after commit

**Task 6.3 — CLAUDE.md Update**:
- [ ] Active Initiatives table: Week 4 = Complete (45/45)
- [ ] AGENTS.md updated
- [ ] Bootstrap file updated
- [ ] MEMORY.md updated

### Output
- Single output report at `04-prompts/06-finalize/02-output/REPORT.md` covering all 3 tasks
