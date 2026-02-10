# Task 4.2 Prompt — Architecture Documentation (6 files)

## Persona
Technical architect documenting the system design for a RAG-based freight forwarding co-pilot. You produce clear architecture documentation with diagrams (Mermaid syntax), data flow descriptions, and API contracts.

## Context
- **Initiative**: enhancement--poc-evaluation
- **Task**: 4.2 — Architecture documentation (6 files)
- **Phase**: 4 (Documentation)
- **Dependencies**: CP3 (PASSED)
- **Blocks**: T4.4 (Documentation index)
- **Workspace**: `pilot_phase1_poc/05_evaluation/`

### Existing Documentation (from Task 4.1)
Task 4.1 created 29 codebase-level docs. Task 4.2 produces higher-level architecture docs that complement them. Avoid duplicating content — reference Layer 3 docs where appropriate (e.g., "See [services.md](../codebase/backend/services.md) for function-level details").

### Tech Stack Summary
| Component | Technology | Version |
|-----------|------------|---------|
| Vector DB | ChromaDB | 0.5.23 |
| Embeddings | all-MiniLM-L6-v2 | via ONNX |
| Document Processing | Python | 3.11+ |
| Backend | Express (Node.js) | 18+ |
| Frontend | React + Tailwind | 18+ |
| LLM | Groq API (Llama 3.1 8B) | llama-3.1-8b-instant |
| Text Splitting | langchain-text-splitters | RecursiveCharacterTextSplitter |
| Markdown Rendering | react-markdown + remark-gfm | — |

## Task

Create **6 architecture documentation files** at `documentation/architecture/`. Use Mermaid diagrams where specified. Read actual source files to verify details — do not guess.

### File 1: `system_overview.md`

**Content:**
- System purpose (RAG co-pilot for freight forwarding CS agents in Singapore/SEA)
- Tech stack table with versions (from above)
- Component diagram (Mermaid) showing:
  - React Frontend (Vite dev server, port 5173)
  - Express API (port 3000)
  - Python subprocess bridge (query_chroma.py, stdin/stdout JSON)
  - ChromaDB (local PersistentClient, ./chroma_db)
  - Groq API (external, llama-3.1-8b-instant)
  - Knowledge Base (30 markdown docs in ./kb/)
- Deployment topology: all local except Groq API
- Key constraints: no live system integration (TMS/WMS), no real-time data, Singapore-centric

### File 2: `data_flow.md`

**Content:**
- End-to-end query flow sequence diagram (Mermaid):
  ```
  User → React UI → POST /api/query → Express → pipeline.js →
    → retrieval.js → spawn Python → query_chroma.py → ChromaDB → chunks →
    → formatContext() → llm.js → Groq API → LLM response →
    → citations.js → processCitations → enrichCitations → buildSources/buildRelatedDocs →
    → calculateConfidence → JSON response → React UI → 4-section card
  ```
- Timing breakdown: retrieval (~200ms subprocess), generation (~800ms Groq), citation (<10ms), total ~1.2s avg
- Data transformations at each stage:
  - Query string → ChromaDB query → chunks with scores
  - Chunks → formatted context string (`[Title > Section]\ncontent`)
  - Context + query → system prompt + user message → LLM response text
  - Response text → extracted citations → enriched citations → sources array
  - All → {answer, sources, relatedDocs, citations, confidence, metadata}
- Error flow: ChromaDB unavailable → Pipeline error; Groq 429 → retry with backoff; Groq 400 → immediate fail

### File 3: `ingestion_pipeline_flow.md`

**Content:**
- Ingestion pipeline flow diagram (Mermaid):
  ```
  KB docs (./kb/) → discover_documents() → parse_frontmatter() → parse_document() →
    → chunk_document() → ChromaDB.add() with embeddings
  ```
- Stage details:
  1. **Discovery**: `discover_documents(path)` — recursively finds .md files, excludes `pdfs/` subdirs
  2. **Parsing**: `parse_document(path)` — YAML frontmatter extraction, body text extraction (frontmatter stripped), 13-field document dict
  3. **Chunking**: `chunk_document(doc)` — RecursiveCharacterTextSplitter(600, 90), separators: `["\n## ", "\n### ", "\n\n", "\n"]`, section/subsection header extraction per chunk
  4. **Embedding**: ChromaDB default (all-MiniLM-L6-v2 via ONNX, 384-d) — automatic, no separate step
  5. **Storage**: ChromaDB PersistentClient, collection `waypoint_kb`, 13 metadata fields per chunk
- Key parameters: CHUNK_SIZE=600, CHUNK_OVERLAP=90, 30 docs → 709 chunks
- Metadata fields stored in ChromaDB: doc_id, title, source_org, source_urls (comma-joined), source_type, last_updated, jurisdiction, category, use_cases (comma-joined), section (header), subsection (header), file_path, chunk_index
- Critical design decision: frontmatter is stripped before embedding — only body text gets embedded. This means retrieval_keywords in frontmatter have NO direct impact on retrieval. Key terms must appear in body text.

### File 4: `rag_pipeline_flow.md`

**Content:**
- RAG pipeline flow diagram (Mermaid):
  ```
  POST /api/query → validate → processQuery() →
    Stage 1: retrieveChunks(query, {topK, threshold}) → Python subprocess → ChromaDB → filter by threshold → chunks
    Stage 2: formatContext(chunks) → context string
    Stage 3: generateResponse(query, context) → buildSystemPrompt(context) → Groq API → parseCompletion → answer
    Stage 4: processCitations(answer, chunks) → extractCitations → enrichCitations → buildSources + buildRelatedDocs
    Stage 5: calculateConfidence(chunks, citationResult) → {level, reason}
    → Build response → JSON
  ```
- Stage details with config values:
  - **Retrieval**: topK=10 (config default), threshold=0.15, Python subprocess spawns query_chroma.py, distance→similarity conversion (score = 1 - distance)
  - **Context Assembly**: `[Title > Section]\ncontent\n\n` format, truncated at maxContextTokens * 4 chars
  - **Generation**: Groq API (OpenAI-compatible), model=llama-3.1-8b-instant, temperature=0.3, max_tokens=500, retry on 429/5xx with exponential backoff (1s base, 10s max, 25% jitter)
  - **Citation Processing**: regex `/\[([^\]]+)\]/g`, 3-tier matching (exact → contains → Dice similarity > 0.5), enrich with sourceUrls/docId/score
  - **Confidence Scoring**: High (>=3 chunks, avgScore>=0.5), Medium (>=2 chunks, avgScore>=0.3), Low (else)
- No-results path: 0 chunks → buildNoResultsResponse (skip LLM call, return Low confidence with decline message)

### File 5: `kb_schema.md`

**Content:**
- YAML frontmatter schema (all fields with types, required/optional, examples):
  ```yaml
  title: string (required) — Document title
  source_org: string (required) — e.g., "Singapore Customs"
  source_urls: list[string] (required) — Primary URLs
  source_type: enum (required) — public_regulatory | public_carrier | synthetic_internal
  last_updated: date (required) — YYYY-MM-DD
  jurisdiction: enum (required) — SG | MY | ID | TH | VN | PH | ASEAN | Global
  category: enum (required) — customs | carrier | policy | procedure | reference
  use_cases: list[string] (optional) — UC-1.1, UC-2.3, etc.
  retrieval_keywords: list[string] (optional) — NOTE: not embedded, body text only
  ```
- Category folder structure:
  - `01_regulatory/` (14 docs) — Singapore Customs, ASEAN trade regulations
  - `02_carriers/` (6 docs) — Ocean & air carrier info (Maersk, MSC, ONE, PIL, etc.)
  - `03_reference/` (3 docs) — Incoterms, HS codes, FTA comparison
  - `04_internal_synthetic/` (6 docs) — Company policies, procedures, SLAs
  - `*/pdfs/` — Reference PDFs (NOT ingested, excluded by discover_documents)
- ChromaDB chunk metadata (13 fields stored per chunk)
- How to add a new document: step-by-step guide (create .md, add frontmatter, place in correct category folder, run `python scripts/ingest.py --clear`, verify with `python scripts/verify_ingestion.py`)
- KB stats: 30 docs, 709 chunks, 92% retrieval hit rate

### File 6: `api_contract.md`

**Content:**
- Base URL: `http://localhost:3000`
- **POST /api/query**:
  - Request: `{ "query": string }` — max 1000 chars, non-empty
  - Response (200):
    ```json
    {
      "answer": "string — markdown-formatted response text",
      "sources": [{ "title": "string", "org": "string", "url": "string", "section": "string|null" }],
      "relatedDocs": [{ "title": "string", "category": "string", "docId": "string", "url": "string|null" }],
      "citations": [{ "raw": "string", "title": "string", "section": "string|null", "matched": true, "sourceUrls": ["string"], "docId": "string", "score": number }],
      "confidence": { "level": "High|Medium|Low", "reason": "string" },
      "metadata": { "query": "string", "chunksRetrieved": number, "chunksUsed": number, "latencyMs": number, "model": "string|null" }
    }
    ```
  - Error responses: 400 (invalid/empty/too long query), 500 (pipeline error)
- **GET /api/health**:
  - Response: `{ "status": "ok", "timestamp": "ISO8601", "uptime": number, "version": "string" }`
- CORS: enabled (all origins)
- Content-Type: application/json
- Body limit: 10kb

### Source Files to Read

| Priority | File | Purpose |
|----------|------|---------|
| HIGH | `backend/services/pipeline.js` | RAG pipeline stages, confidence scoring |
| HIGH | `backend/services/retrieval.js` | ChromaDB bridge, formatContext |
| HIGH | `backend/services/llm.js` | Groq client, retry, buildSystemPrompt |
| HIGH | `backend/services/citations.js` | Citation pipeline, buildSources/buildRelatedDocs |
| HIGH | `backend/config.js` | All config values |
| HIGH | `backend/routes/query.js` | API contract, validation |
| HIGH | `scripts/config.py` | Python-side config |
| HIGH | `scripts/process_docs.py` | Document parsing |
| HIGH | `scripts/chunker.py` | Chunking algorithm |
| MED | `scripts/ingest.py` | Ingestion entry |
| MED | `scripts/query_chroma.py` | Python bridge |

## Validation
- [ ] 6 architecture docs created
- [ ] `system_overview.md` includes tech stack with versions + component diagram
- [ ] `data_flow.md` includes sequence diagram (Mermaid)
- [ ] `ingestion_pipeline_flow.md` covers all stages with config parameters
- [ ] `rag_pipeline_flow.md` covers all stages with config parameters
- [ ] `kb_schema.md` covers all frontmatter fields and ChromaDB metadata
- [ ] `api_contract.md` covers new 4-section response shape with full JSON schema

## Output

Create output report: `04-prompts/04-documentation/task_4_2/02-output/TASK_4.2_OUTPUT.md`

## Update on Completion

**MANDATORY — Update ALL 7 tracking locations:**
1. **Checklist**: `03-checklist/IMPLEMENTATION_CHECKLIST.md` — mark T4.2 `[x]`, update Phase 4 progress (2/9), Total (30/45, 67%)
2. **Roadmap Progress Tracker**: Phase 4 → `2`, Total → `30 | 67%`
3. **Roadmap Quick Reference**: T4.2 → `✅ Complete`
4. **Roadmap Detailed Entry**: T4.2 Status → `✅ Complete`, validation checkboxes `[x]`
5. **Bootstrap file**: `ai-workflow-bootstrap-prompt-v3.md` → `30/45 -- 67%`
6. **CLAUDE.md** (root): → `30/45 — 67%`
7. **AGENTS.md** (root): → `30/45 -- 67%`
