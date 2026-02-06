# Task 9: Update RAG Pipeline to Use New KB

## Persona

You are a DevOps engineer integrating a newly optimized knowledge base into an existing RAG pipeline. You need to replace the Week 2 ChromaDB with the Week 3 optimized version without breaking the running system. The RAG pipeline is a Node.js + Python hybrid: Express backend calls a Python subprocess (`query_chroma.py`) to query ChromaDB.

## Context

### What Changed in Week 3

The retrieval optimization (Tasks 1-8) produced a significantly improved knowledge base:

| Metric | Week 2 (03_rag_pipeline) | Week 3 (04_retrieval_optimization) |
|--------|:------------------------:|:----------------------------------:|
| Documents | 29 | **30** (+1 customer_faq) |
| Chunks | ~400 | **709** |
| Hit rate | 76% raw | **94% raw** |
| Config | 600/90/top_k=5 | **600/90/top_k=5** (unchanged) |

Key improvements in the KB:
- All 30 docs have "Key Terms and Abbreviations" body sections (abbreviation-to-full-term mappings)
- All 30 docs have `retrieval_keywords` in frontmatter
- New `customer_faq.md` document (consolidates common Q&A)
- FCL vs LCL comparison section added to `booking_procedure.md`
- Form D vs Form AK comparison section added to `fta_comparison_matrix.md`
- PDF extracts excluded from ingestion (reference only, in `pdfs/` subdirs)
- Placeholder text fixed ([Company Name], phone numbers, emails)

### Architecture

```
03_rag_pipeline/
├── .env                    ← CHROMA_PATH=./ingestion/chroma_db
├── src/                    ← Node.js Express backend (port 3000)
│   ├── services/
│   │   ├── retrieval.js    ← Calls Python subprocess: query_chroma.py
│   │   ├── llm.js          ← Groq Llama 3.1 8B
│   │   ├── pipeline.js     ← RAG orchestration
│   │   └── citations.js    ← Citation extraction
│   └── routes/
│       └── query.js        ← POST /api/query
├── ingestion/
│   ├── chroma_db/          ← ChromaDB storage (TO BE REPLACED)
│   ├── scripts/
│   │   ├── query_chroma.py ← Python query bridge (used by retrieval.js)
│   │   ├── config.py       ← CHROMA_PERSIST_PATH=./chroma_db
│   │   └── ...
│   └── .env                ← CHUNK_SIZE=600, CHUNK_OVERLAP=90
├── kb/                     ← Week 2 KB (29 docs, sub-subdirectories)
├── client/                 ← React + Vite frontend
└── tests/                  ← Jest tests + E2E Python tests
```

```
04_retrieval_optimization/
├── chroma_db/              ← Optimized ChromaDB (TO COPY FROM)
├── kb/                     ← Week 3 KB (30 docs, flat category folders)
└── scripts/                ← Forked ingestion pipeline
```

### Important Notes

1. **Chunk params unchanged**: Both pipelines use CHUNK_SIZE=600, CHUNK_OVERLAP=90, collection `waypoint_kb`. No config changes needed.

2. **KB folder structure differs**:
   - Week 2: `kb/01_regulatory/singapore_customs/sg_gst_guide.md` (sub-subdirectories)
   - Week 3: `kb/01_regulatory/sg_gst_guide.md` (flat category folders)
   - This does NOT affect ChromaDB — doc_ids use `{category}_{filename}` format which resolves the same either way.

3. **`query_chroma.py` in 03_rag_pipeline** reads from `ingestion/chroma_db/` and returns chunk text + metadata. It does NOT read KB files directly. Replacing ChromaDB is sufficient.

4. **The `file_path` metadata** stored in ChromaDB chunks will point to `04_retrieval_optimization/kb/...` paths. This is cosmetic — the RAG pipeline uses chunk text for context, not file paths. The citation system uses `doc_id` and `title` metadata, not file paths.

5. **Node.js test expectations** may need updating if they assert specific retrieval results or chunk counts.

## Task

### Step 1: Back Up Existing ChromaDB

```bash
cd pilot_phase1_poc/03_rag_pipeline/ingestion

# Create backup
cp -r chroma_db chroma_db_backup_week2
```

Verify backup exists and has content (chroma.sqlite3 file).

### Step 2: Replace ChromaDB

```bash
# Remove old ChromaDB
rm -rf pilot_phase1_poc/03_rag_pipeline/ingestion/chroma_db

# Copy optimized ChromaDB from Week 3
cp -r pilot_phase1_poc/04_retrieval_optimization/chroma_db pilot_phase1_poc/03_rag_pipeline/ingestion/chroma_db
```

Verify the new ChromaDB:
```bash
cd pilot_phase1_poc/03_rag_pipeline/ingestion
# Check file exists
ls -la chroma_db/chroma.sqlite3
```

### Step 3: Verify ChromaDB Content

Use the existing `view_chroma.py` or write a quick Python check:

```bash
cd pilot_phase1_poc/03_rag_pipeline/ingestion
venv/Scripts/python -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_db')
col = client.get_collection('waypoint_kb')
print(f'Collection: waypoint_kb')
print(f'Chunks: {col.count()}')
# Expect 709 chunks
"
```

**Expected**: 709 chunks (was ~400 in Week 2).

### Step 4: Quick Retrieval Smoke Test

Test a few queries to confirm retrieval works through the Python bridge:

```bash
cd pilot_phase1_poc/03_rag_pipeline/ingestion
venv/Scripts/python -m scripts.query_chroma "What's the difference between FCL and LCL?" 3
```

**Expected**: Top result should be `booking_procedure` with the new FCL vs LCL comparison section (similarity ~0.69).

Also test:
```bash
venv/Scripts/python -m scripts.query_chroma "What's the difference between Form D and Form AK?" 3
```

**Expected**: Top result should be `fta_comparison_matrix` (similarity ~0.77).

### Step 5: Copy Updated KB Files (Optional but Recommended)

While not strictly required (the RAG pipeline reads from ChromaDB, not KB files), keeping the KB in sync is good hygiene:

```bash
# Back up old KB
mv pilot_phase1_poc/03_rag_pipeline/kb pilot_phase1_poc/03_rag_pipeline/kb_backup_week2

# Copy Week 3 KB (excluding pdfs/ subdirectories)
# Note: The 03_rag_pipeline expects sub-subdirectories but doc_ids resolve the same
# Using the flat structure from Week 3 is fine for reference
cp -r pilot_phase1_poc/04_retrieval_optimization/kb pilot_phase1_poc/03_rag_pipeline/kb
```

**Important**: Do NOT copy `pdfs/` subdirectories — they are large reference files not needed by the RAG pipeline. Either:
- Use `rsync --exclude='pdfs/'` if available
- Or copy and then remove: `find pilot_phase1_poc/03_rag_pipeline/kb -type d -name pdfs -exec rm -rf {} +`

### Step 6: Start Server and Manual Smoke Test

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Start the backend
npm start
```

In a separate terminal (or use the client):
```bash
# Test the API endpoint
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the difference between FCL and LCL?"}'
```

**Verify**:
- Server starts without errors
- Response includes answer text
- Response cites `booking_procedure` as a source
- Citations include the new FCL vs LCL comparison content

Also test:
```bash
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I file a claim for damaged cargo?"}'
```

**Verify**: Response cites `service_terms_conditions` Section 8 (Claims).

### Step 7: Run Test Suites

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Run Node.js Jest tests
npm test

# Run E2E tests (if configured)
cd tests/e2e
python test_runner.py
```

**Handle test failures**:
- If retrieval tests fail due to changed chunk counts or retrieval order, update the test expectations to match the new 709-chunk collection.
- If citation tests fail, verify the citation extraction logic still works with the new chunk metadata format (should be identical).
- If E2E tests have hardcoded expected sources, update them to reflect the improved retrieval.

### Step 8: Run Verification Tests

```bash
cd pilot_phase1_poc/03_rag_pipeline/ingestion
venv/Scripts/python -m scripts.verify_ingestion --verbose
```

**Note**: `verify_ingestion.py` was written for the Week 2 KB (29 docs). It may need updates for:
- Document count: 29 → 30 (customer_faq added)
- Chunk count expectations
- Any hardcoded doc_id references

If verification fails on count, check if it's just the expected numbers that need updating.

## Format

### Execution Order

1. Back up existing ChromaDB and KB
2. Copy new ChromaDB from 04_retrieval_optimization
3. Verify chunk count (expect 709)
4. Quick Python retrieval smoke test
5. Copy updated KB files (exclude pdfs/)
6. Start server + manual API smoke test
7. Run test suites (fix expectations if needed)
8. Run verification tests (fix expectations if needed)

### Commands Summary

```bash
# All commands from project root: pilot_phase1_poc/

# Step 1: Backup
cp -r 03_rag_pipeline/ingestion/chroma_db 03_rag_pipeline/ingestion/chroma_db_backup_week2

# Step 2: Replace
rm -rf 03_rag_pipeline/ingestion/chroma_db
cp -r 04_retrieval_optimization/chroma_db 03_rag_pipeline/ingestion/chroma_db

# Step 3: Verify
cd 03_rag_pipeline/ingestion
venv/Scripts/python -c "import chromadb; c=chromadb.PersistentClient(path='./chroma_db'); print(c.get_collection('waypoint_kb').count())"

# Step 4: Smoke test
venv/Scripts/python -m scripts.query_chroma "What's the difference between FCL and LCL?" 3

# Step 5: Copy KB
cd ../..
mv 03_rag_pipeline/kb 03_rag_pipeline/kb_backup_week2
cp -r 04_retrieval_optimization/kb 03_rag_pipeline/kb

# Step 6: Start server
cd 03_rag_pipeline && npm start

# Step 7: Run tests
npm test
```

### Output Report

Save the output report to:
```
04-prompts/04-refinement/task_9_rag_pipeline_update/02-output/REPORT.md
```

Report structure:
1. **Summary**: ChromaDB replaced, server running, tests status
2. **Backup**: What was backed up and where
3. **Verification**: Chunk count, smoke test results
4. **Test Results**: Which tests passed/failed, what was fixed
5. **Issues**: Any problems encountered and how resolved

Also update:
- `IMPLEMENTATION_ROADMAP.md` — mark Task 9 complete
- `IMPLEMENTATION_CHECKLIST.md` — mark Task 9 items
