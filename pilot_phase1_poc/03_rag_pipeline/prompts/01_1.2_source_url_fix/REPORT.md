# Task 1.2: Fix source_urls in Ingestion - Output Report

**Completed**: 2026-01-30 11:15
**Status**: Complete

---

## Summary

Successfully updated `ingest.py` to include `source_urls` in ChromaDB metadata. Re-ingested all 29 documents (483 chunks) with the `--clear` flag. Verified that:
- Regulatory documents (Singapore Customs) have correct source URLs
- Internal/synthetic documents have empty string for source_urls
- All 483 chunks now include the source_urls field in metadata

---

## Files Created/Modified

| File | Action | Path |
|------|--------|------|
| scripts/ingest.py | Modified | `pilot_phase1_poc/03_rag_pipeline/ingestion/scripts/ingest.py` |
| chroma_db/ | Updated (re-ingested) | `pilot_phase1_poc/03_rag_pipeline/ingestion/chroma_db/` |

### Change Details

**ingest.py (line 148)**: Added `source_urls` field to metadata dict:
```python
"source_urls": ",".join(chunk.get("source_urls", [])),
```

This converts the list of URLs from document frontmatter to a comma-separated string for ChromaDB storage.

---

## Acceptance Criteria

- [x] `ingest.py` updated to include `source_urls` in metadata dict
- [x] Re-ingestion complete with `--clear` flag (483 chunks)
- [x] Query confirms `source_urls` field exists in metadata
- [x] Regulatory docs (Singapore Customs) have correct URLs
- [x] Internal/synthetic docs have empty string for source_urls

---

## Verification Results

### Metadata Keys
```
['category', 'chunk_index', 'doc_id', 'file_path', 'jurisdiction', 
 'section_header', 'source_org', 'source_type', 'source_urls', 
 'subsection_header', 'title']
```

### Sample: Singapore Customs Document
- **Title**: Singapore Certificates of Origin
- **Source URLs**: `https://www.customs.gov.sg/businesses/rules-of-origin/origin-documentation/,https://www.enterprisesg.gov.sg/...`

### Sample: Internal Document
- **Title**: Service Terms and Conditions
- **Source URLs**: `''` (empty string as expected)

### Total Chunks
- **Count**: 483 chunks in ChromaDB

---

## Issues Encountered

None. The `where={'category': 'customs'}` query returned no results because the category field uses values like `regulatory`, `carrier`, `reference`, etc. Used `source_org` filter instead to verify regulatory documents.

---

## Next Steps

Proceed to **Task 2.1: Create Retrieval Quality Test Script** - Build a test script that runs 50 test queries against ChromaDB and generates quality reports.
