# Task 4.3 Prompt — User-Facing Guides (3 files)

## Persona
Technical writer producing practical, audience-appropriate documentation. You write clear, actionable guides — concise for end users, detailed for developers.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Task**: 4.3 — User-facing guides (3 files)
- **Phase**: 4 (Documentation)
- **Dependencies**: CP3 (PASSED)
- **Blocks**: T4.4 (Documentation index)
- **Workspace**: `pilot_phase1_poc/05_evaluation/`

### Existing Documentation
Tasks 4.1 (29 codebase docs) and 4.2 (6 architecture docs) are complete. Task 4.3 produces user-facing guides that complement them. Reference architecture docs where appropriate (e.g., "See [api_contract.md](../architecture/api_contract.md) for full API specification").

## Task

Create **3 user-facing guide files** at `documentation/guides/`. Read actual source files to verify details — do not guess.

### File 1: `user_guide.md`

**Audience**: Customer service agents using the system daily.

**Content:**
- **What is Waypoint Co-Pilot?** — One paragraph: RAG-based assistant for freight forwarding CS agents, answers questions about customs, carriers, booking procedures, and policies for Singapore/SEA
- **How to Ask Effective Questions**:
  - Be specific: "What documents are needed for importing electronics to Singapore?" > "import docs"
  - Include context: mention country, carrier, or regulation name when relevant
  - One question at a time — the system handles single queries, not multi-turn conversations
  - Use natural language — no special syntax needed
- **Understanding the Response Card** — explain each of the 4 sections:
  1. **Answer** — Markdown-formatted response with inline citations in `[Document Title]` format. Citations link to source documents. May include headers, lists, bold text for key terms.
  2. **Sources** — Clickable links to the original regulatory websites or carrier pages that the answer draws from. Shows organization name and domain.
  3. **Related Documents** — Category-colored chips showing all KB documents relevant to your query (not just the ones cited). Categories: regulatory (blue), carrier (amber), reference (green), internal (gray).
  4. **Confidence Footer** — Color-coded badge:
     - **High** (green): 3+ strong sources found — answer is well-supported
     - **Medium** (amber): 2+ sources with moderate relevance — verify for critical decisions
     - **Low** (red): Limited sources — treat as guidance only, confirm with specialist
     - Also shows: chunks retrieved, chunks used, response time
- **When to Escalate** — the co-pilot CANNOT help with:
  - Real-time shipment tracking → use tracking portal
  - Live freight rate quotes → contact sales team
  - Booking modifications or cancellations → contact account manager
  - Account-specific data → customer portal or account manager
  - Actions (book, cancel, track, order) → system provides information only
  - If confidence is "Low" on a critical question → verify with subject matter expert
- **Sample Queries** — provide 8-10 examples across different categories:
  1. "What documents are needed to import goods into Singapore?" (regulatory)
  2. "What is the GST rate for imported goods in Singapore?" (regulatory)
  3. "What Incoterms 2020 terms are commonly used for sea freight?" (reference)
  4. "What ocean routes does Maersk offer from Singapore?" (carrier)
  5. "What is the booking lead time for ocean freight?" (internal procedure)
  6. "What are the SLA response times for customer inquiries?" (internal policy)
  7. "How do I classify goods using HS codes?" (reference)
  8. "What are Singapore's rules of origin requirements for FTA benefits?" (regulatory)
  9. "What dangerous goods restrictions apply to air cargo?" (regulatory)
  10. "What are the escalation procedures for urgent shipment issues?" (internal)

### File 2: `deployment_notes.md`

**Audience**: Developers and IT staff setting up the system.

**Content:**
- **Prerequisites**:
  - Node.js 18+ (with npm)
  - Python 3.11+ (with pip and venv)
  - Git
  - Groq API key (free tier available at https://console.groq.com)
  - ~500MB disk space (ChromaDB + ONNX model + node_modules + venv)
- **Installation Steps** (numbered, copy-pasteable commands):
  1. Clone the repository
  2. Navigate to `pilot_phase1_poc/05_evaluation/`
  3. Python setup: `py -3.11 -m venv venv` → activate → `pip install -r requirements.txt`
  4. Node.js setup: `npm install`
  5. Frontend setup: `cd client && npm install`
  6. Create `.env` file from `.env.example` with required variables
- **Environment Configuration** — full `.env` reference:
  ```
  # Required
  LLM_API_KEY=gsk_...                    # Groq API key (required for LLM calls)

  # Optional (defaults shown)
  PORT=3000                               # Express server port
  NODE_ENV=development                    # development | production | test
  CHROMA_PATH=./chroma_db                 # ChromaDB storage directory
  COLLECTION_NAME=waypoint_kb             # ChromaDB collection name
  RETRIEVAL_TOP_K=10                      # Number of chunks to retrieve
  RELEVANCE_THRESHOLD=0.15               # Minimum similarity score
  MAX_CONTEXT_TOKENS=2000                 # Max tokens for LLM context
  LLM_PROVIDER=groq                       # LLM provider
  LLM_BASE_URL=https://api.groq.com/openai/v1
  LLM_MODEL=llama-3.1-8b-instant         # LLM model
  LLM_TEMPERATURE=0.3                     # LLM temperature (0-1)
  LLM_MAX_TOKENS=500                      # Max response tokens

  # Python-side (in .env at project root)
  CHUNK_SIZE=600                          # Characters per chunk
  CHUNK_OVERLAP=90                        # Overlap between chunks
  KNOWLEDGE_BASE_PATH=./kb                # KB directory
  CHROMA_PERSIST_PATH=./chroma_db         # ChromaDB directory
  LOG_LEVEL=INFO                          # Python logging level
  ```
- **Running Ingestion** (one-time or when KB changes):
  ```bash
  # Activate Python venv first
  python scripts/ingest.py --clear        # Clear and rebuild vector store
  python scripts/verify_ingestion.py      # Verify: should show 30 docs, ~709 chunks
  ```
- **Starting the System**:
  ```bash
  # Terminal 1: Backend API
  npm start                               # Express on http://localhost:3000

  # Terminal 2: Frontend
  cd client && npm run dev                # Vite on http://localhost:5173
  ```
  Open `http://localhost:5173` in a browser.
- **Running Tests**:
  ```bash
  npm test                                # Jest backend tests (162 tests)
  cd client && npm test                   # Vitest frontend tests
  python -m pytest tests/ -v             # Python ingestion tests (55 tests)
  python scripts/retrieval_quality_test.py  # 50-query retrieval hit rate test
  ```
- **Troubleshooting** — common issues:

  | Problem | Cause | Solution |
  |---------|-------|----------|
  | `LLM_API_KEY environment variable is required` | Missing .env or key | Create `.env` with `LLM_API_KEY=gsk_...` |
  | `Python query failed` on first query | ChromaDB not ingested | Run `python scripts/ingest.py --clear` |
  | `ECONNREFUSED` on frontend | Backend not running | Start backend first with `npm start` |
  | Port 3000 already in use | Stale process | Kill it: `netstat -ano \| findstr :3000` then `taskkill /PID <pid> /F` |
  | Port 5173 already in use | Stale Vite process | Same approach as above for port 5173 |
  | `Failed to spawn Python process` | Wrong Python path or no venv | Verify `venv/Scripts/python.exe` exists, re-create venv if needed |
  | Groq 429 (rate limit) | Too many requests | Wait 60s; free tier has ~30 req/min limit |
  | `No relevant chunks found` for valid query | ChromaDB empty or corrupted | Re-run ingestion: `python scripts/ingest.py --clear` |
  | Frontend shows CORS error | Backend not running or wrong port | Ensure backend is running on port 3000 |

### File 3: `known_limitations.md`

**Audience**: All stakeholders — sets honest expectations about what the POC can and cannot do.

**Content:**
- **Scope Limitations** (by design for POC):
  - No live system integration (TMS, WMS, tracking systems, booking platforms)
  - No real-time data (freight rates, shipment status, inventory)
  - No multi-turn conversation — each query is independent, no session memory
  - No authentication or authorization — no user accounts, roles, or access control
  - No audit trail — queries and responses are not persisted
  - Singapore-centric — regulatory content focuses on Singapore Customs with limited SEA secondary coverage
  - English only — no multilingual support
- **Technical Limitations**:
  - Single LLM model (Llama 3.1 8B via Groq) — no fallback if Groq API is unavailable
  - Groq free tier rate limits (~30 requests/minute) — not suitable for production load
  - Python subprocess per query — adds ~200ms latency overhead vs native DB client
  - Local ChromaDB — not suitable for multi-user or distributed deployment
  - No caching — identical queries re-run the full pipeline each time
  - No streaming — full response generated before display (typically ~1.2s total)
  - Max 500 output tokens — very long answers may be truncated
- **Knowledge Base Limitations**:
  - Static content only — documents are point-in-time snapshots, not auto-updated
  - 30 documents / 709 chunks — limited breadth; some niche topics may not be covered
  - Retrieval hit rate: 92% (50-query test suite) — ~4 queries in 50 may not find relevant chunks
  - Abbreviation-dependent queries may miss if the abbreviation isn't in document body text
  - PDF content selectively merged — some detailed regulatory annexes not fully captured
- **Evaluation Gaps** (identified during Round 4 evaluation):
  - Citation accuracy at 80.5% (target: ≥80%) — borderline, with 10 applicable queries having reclassified `applicable` flags
  - Hallucination rate at 10% — under target (<15%) but 5/50 queries produced unverifiable claims
  - Some carrier-specific questions return general industry answers rather than carrier-specific details
  - Confidence scoring thresholds were lowered (High: 0.6→0.5, Medium: 0.4→0.3) to achieve reasonable distribution — may overstate confidence for marginal queries
- **Out-of-Scope Query Categories** (system politely declines):
  - Real-time tracking requests
  - Live freight rate quotes
  - Booking/order/cancellation actions
  - Account-specific data inquiries
  - System actions (book, cancel, track, modify, submit)
- **Recommendations for Production** (brief, forward-looking):
  - Add LLM fallback (e.g., OpenAI GPT-4o-mini as backup)
  - Implement query caching for common questions
  - Add user authentication and query logging
  - Schedule regular KB content refreshes
  - Consider managed vector DB (Pinecone, Weaviate Cloud) for scalability
  - Add multi-turn conversation support with session context

### Source Files to Read

| Priority | File | Purpose |
|----------|------|---------|
| HIGH | `backend/config.js` | All environment variables and defaults |
| HIGH | `backend/prompts/system.txt` | System prompt — out-of-scope handling |
| HIGH | `.env.example` | Existing env example file |
| HIGH | `package.json` | Node.js scripts and dependencies |
| HIGH | `client/package.json` | Frontend scripts and dependencies |
| HIGH | `requirements.txt` | Python dependencies |
| MED | `documentation/architecture/api_contract.md` | API response shape for user guide |
| MED | `documentation/architecture/system_overview.md` | Tech stack for deployment notes |
| MED | `data/evaluation_results_round4.json` | Evaluation results for known limitations |

## Validation
- [ ] User guide covers CS agent workflow
- [ ] User guide explains 4-section response card
- [ ] Deployment notes cover full installation from scratch
- [ ] Deployment notes include troubleshooting section
- [ ] Known limitations comprehensive and honest
- [ ] All 3 files created

## Output

Create output report: `04-prompts/04-documentation/task_4_3/02-output/TASK_4.3_OUTPUT.md`

## Update on Completion

**MANDATORY — Update ALL 7 tracking locations:**
1. **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark T4.3 `[x]`, update Phase 4 progress (3/9), Total (31/45, 69%)
2. **Roadmap Progress Tracker**: Phase 4 → `3`, Total → `31 | 69%`
3. **Roadmap Quick Reference**: T4.3 → `✅ Complete`
4. **Roadmap Detailed Entry**: T4.3 Status → `✅ Complete`, validation checkboxes `[x]`
5. **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` → `31/45 -- 69%`
6. **CLAUDE.md** (root): → `31/45 — 69%`
7. **AGENTS.md** (root): → `31/45 -- 69%`
