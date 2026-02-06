# Task 6 Pass 2: PDF Discovery via Chrome DevTools MCP

## Persona

**Role**: Senior Content Engineer / Knowledge Base Architect

**Expertise**:
- Web scraping and PDF discovery via Chrome DevTools MCP browser automation
- Knowledge base design for RAG retrieval systems
- YAML frontmatter and markdown formatting
- Freight forwarding and customs documentation
- Singapore trade regulations and ASEAN trade frameworks

---

## Context

### Background

Pass 1 is **COMPLETE** — all 30 markdown documents exist in `04_retrieval_optimization/kb/`:
- 24 CARRY FORWARD docs copied
- 5 ENRICH docs with new content (Fixes 1-9)
- 1 new FAQ created (`customer_faq.md`)

**What remains**: Pass 2 — PDF Discovery. Visit ~70 source URLs via **Chrome DevTools MCP**, scan for downloadable PDFs, download them, extract with `pdf_extractor.py`, and merge useful content into existing KB docs.

### Why PDF Discovery Matters

The original KB was built from web scraping only. Government agencies, trade bodies, and carriers often publish detailed guides, tariff schedules, and procedures as PDFs not captured by text scraping. These PDFs may contain:
- Detailed customs procedures and forms
- Tariff schedules and HS code lookup tables
- Carrier service guides, container specs, and rate cards
- Trade agreement annexes and rules of origin details

This content could address the 9 previously failing queries and improve overall retrieval quality.

### Tool: Chrome DevTools MCP

**IMPORTANT**: Use `mcp__chrome-devtools__*` tools (NOT `mcp__claude-in-chrome__*`).

Key tools and their usage:

| Tool | Purpose |
|------|---------|
| `navigate_page` | Navigate to each source URL (`type: "url"`, `url: "<url>"`) |
| `take_snapshot` | Get accessible text tree of the page (preferred over screenshots) |
| `take_screenshot` | Visual check when snapshot is insufficient |
| `evaluate_script` | Run JavaScript to extract all PDF links: `document.querySelectorAll('a[href$=".pdf"]')` |
| `click` | Click elements by uid (from snapshot) |
| `press_key` | Keyboard actions if needed |

### PDF Link Discovery Script

Use this JavaScript via `evaluate_script` on every page to find PDF links:

```javascript
() => {
  // Find all links ending in .pdf
  const pdfLinks = Array.from(document.querySelectorAll('a[href*=".pdf"]'));
  // Also find links with "download" in text/class
  const downloadLinks = Array.from(document.querySelectorAll('a'))
    .filter(a => /download|document|guide|form|circular/i.test(a.textContent + ' ' + a.className));

  const results = {
    pdfLinks: pdfLinks.map(a => ({ href: a.href, text: a.textContent.trim() })),
    downloadLinks: downloadLinks
      .filter(a => !pdfLinks.includes(a))
      .map(a => ({ href: a.href, text: a.textContent.trim() }))
  };
  return results;
}
```

### PDF Download Strategy

Since Chrome DevTools MCP cannot directly download files to disk, use this approach:
1. **Discover PDF URLs** via `evaluate_script` on each page
2. **Log all discovered PDF URLs** to `reports/pdf_discovery_log.md`
3. **Download PDFs** using `navigate_page` to the PDF URL (browser will download or display)
4. **Alternative**: Use Bash `curl` or `Invoke-WebRequest` to download PDFs directly to `kb/<category>/pdfs/`
5. **Extract**: Run `python scripts/pdf_extractor.py <pdf_file>` on downloaded PDFs
6. **Merge**: If content is HIGH/MEDIUM quality and relevant, append to the appropriate KB doc

### Current State

- **30 KB docs**: All present in `04_retrieval_optimization/kb/` (Pass 1 complete)
- **PDF folders**: `kb/{01_regulatory,02_carriers,03_reference,04_internal_synthetic}/pdfs/` exist and are empty
- **PDF Extractor**: `scripts/pdf_extractor.py` ready (single + batch mode, quality flags)
- **Chrome DevTools MCP**: Connected and operational
- **Permissions**: User has granted blanket permission for ALL Chrome DevTools MCP operations — no confirmation needed

### References

| Document | Path | Purpose |
|----------|------|---------|
| Revised Document List | `04_retrieval_optimization/REVISED_DOCUMENT_LIST.md` | Content specs per document |
| Audit Report | `04_retrieval_optimization/reports/01_audit_report.md` | Root cause details |
| PDF Discovery Log | `04_retrieval_optimization/reports/pdf_discovery_log.md` | Track progress (update in-place) |
| Scraping Issues Log | `04_retrieval_optimization/reports/scraping_issues_log.md` | Log problems |

---

## Task

### Objective

Visit ALL ~70 source URLs via Chrome DevTools MCP, discover downloadable PDFs, download and extract them, and merge useful content into the existing KB documents.

### Execution Order

Execute sub-tasks in this order (highest impact first):

1. **6a** — Singapore Customs (~8 URLs) — highest priority, addresses most failing queries
2. **6b** — ASEAN Trade (~8 URLs)
3. **6d** — Ocean Carriers (~18 URLs) — carrier PDFs are high-value
4. **6e** — Air Carriers (~10 URLs)
5. **6c** — Country-specific (~18 URLs)
6. **6f** — Reference (~8 URLs)

*(6g Synthetic Internal has no URLs — skip)*

---

### Sub-task 6a: Singapore Customs (~8 URLs)

**URLs to visit**:
1. https://www.customs.gov.sg/businesses/exporting-goods/overview/
2. https://www.customs.gov.sg/businesses/importing-goods/overview/
3. https://www.customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst/
4. https://www.customs.gov.sg/businesses/rules-of-origin/origin-documentation/
5. https://www.customs.gov.sg/businesses/importing-goods/import-procedures/depositing-goods-in-ftz/
6. https://www.customs.gov.sg/businesses/customs-schemes-licences-and-framework/ftz-operator-licence/
7. https://www.customs.gov.sg/businesses/harmonised-system-classification-of-goods/understanding-hs-classification

**Target KB docs**: `kb/01_regulatory/sg_*.md`
**PDF folder**: `kb/01_regulatory/pdfs/`
**Relevant PDFs**: Customs procedures, HS classification guides, GST guides, import/export forms, FTZ procedures, certificates of origin. **Skip**: annual reports, press releases, recruitment.

---

### Sub-task 6b: ASEAN Trade (~8 URLs)

**URLs to visit**:
1. https://asean.org/our-communities/economic-community/trade-in-goods/
2. https://asean.org/our-communities/economic-community/rules-of-origin/
3. https://tariff-finder.asean.org
4. https://atr.asean.org
5. https://asw.asean.org
6. https://acts.asean.org

**Target KB docs**: `kb/01_regulatory/atiga_*.md`, `kb/01_regulatory/asean_*.md`
**PDF folder**: `kb/01_regulatory/pdfs/`
**Relevant PDFs**: ATIGA agreement text, tariff schedules, rules of origin annexes, Form D templates.

---

### Sub-task 6c: Country-Specific (~18 URLs)

**URLs to visit**:
1. https://www.trade.gov/country-commercial-guides/indonesia-import-requirements-and-documentation
2. https://www.insw.go.id/
3. https://www.beacukai.go.id/
4. https://www.trade.gov/country-commercial-guides/malaysia-import-requirements-and-documentation
5. https://www.customs.gov.my/
6. https://www.miti.gov.my/
7. https://www.trade.gov/country-commercial-guides/thailand-import-requirements-and-documentation
8. https://www.customs.go.th/
9. https://www.trade.gov/country-commercial-guides/vietnam-import-requirements-and-documentation
10. https://www.customs.gov.vn/
11. https://www.vietnamtradeportal.gov.vn/
12. https://www.trade.gov/country-commercial-guides/philippines-import-requirements-and-documentation
13. https://customs.gov.ph/
14. https://www.dti.gov.ph/

**Target KB docs**: `kb/01_regulatory/{country}_import_requirements.md`
**PDF folder**: `kb/01_regulatory/pdfs/`
**Relevant PDFs**: Import requirement guides, tariff schedules, prohibited goods lists, documentation templates.

---

### Sub-task 6d: Ocean Carriers (~18 URLs)

**URLs to visit**:
1. https://www.pilship.com/about-pil/
2. https://www.pilship.com/shipping-solutions/overview/
3. https://www.pilship.com/tariffs-charges/
4. https://www.maersk.com/about
5. https://www.maersk.com/local-information/asia-pacific/singapore
6. https://www.maersk.com/schedules/
7. https://www.maersk.com/logistics-solutions
8. https://sg.one-line.com/about-us
9. https://sg.one-line.com/service-maps
10. https://sg.one-line.com/dry-containers
11. https://www.evergreen-marine.com.sg/tbi1/jsp/TBI1_CorporateProfile.jsp
12. https://ss.shipmentlink.com/tvs2/jsp/TVS2_LongTermMenu.jsp?type=L
13. https://www.evergreen-marine.com.sg/tei1/jsp/TEI1_Containers.jsp

**Target KB docs**: `kb/02_carriers/{carrier}_service_summary.md`
**PDF folder**: `kb/02_carriers/pdfs/`
**Relevant PDFs**: Service guides, container specs, tariff/surcharge PDFs, VGM guides, booking/SI templates. **Skip**: investor presentations, CSR reports.

---

### Sub-task 6e: Air Carriers (~10 URLs)

**URLs to visit**:
1. https://www.siacargo.com/our-company/
2. https://www.siacargo.com/products/
3. https://www.siacargo.com/products/thrucool/
4. https://www.siacargo.com/products/thrufresh/
5. https://www.siacargo.com/network/
6. https://www.cathaycargo.com/en-us/about-us.html
7. https://www.cathaycargo.com/en-us/solutions/cathay-pharma.html
8. https://www.cathaycargo.com/en-us/solutions/cathay-fresh.html
9. https://www.cathaycargo.com/en-us/solutions/cathay-live-animal.html

**Target KB docs**: `kb/02_carriers/{carrier}_service_guide.md`
**PDF folder**: `kb/02_carriers/pdfs/`
**Relevant PDFs**: Product brochures, acceptance checklists, ULD specs, DG guides, temperature-controlled shipping guides.

---

### Sub-task 6f: Reference (~8 URLs)

**URLs to visit**:
1. https://iccwbo.org/business-solutions/incoterms-rules/
2. https://iccwbo.org/ressources-for-business-2/incoterms-rules/incoterms-2020/
3. https://iccwbo.org/ressources-for-business-2/incoterms-rules/incoterms-rules-history/
4. https://www.wcoomd.org/en/topics/nomenclature/overview.aspx
5. https://www.wcoomd.org/en/topics/nomenclature/overview/what-is-the-harmonized-system.aspx
6. https://www.wcoomd.org/en/topics/nomenclature/overview/hs-multi-purposes-tool.aspx

**Target KB docs**: `kb/03_reference/*.md`
**PDF folder**: `kb/03_reference/pdfs/`
**Relevant PDFs**: Incoterms 2020 reference charts, HS nomenclature explanatory notes, classification guides.

---

### Per-URL Workflow

```
For each source URL:
  1. navigate_page → URL
  2. take_snapshot → read page structure
  3. evaluate_script → run PDF discovery JavaScript
  4. IF PDF links found:
     a. Log PDF URL, title, relevance assessment
     b. Download via Bash (curl/Invoke-WebRequest) to kb/<category>/pdfs/
     c. Run: python scripts/pdf_extractor.py <pdf_file>
     d. Review quality flag (HIGH/MEDIUM/LOW)
     e. If HIGH/MEDIUM and useful → append to relevant KB doc, update frontmatter
     f. If LOW or irrelevant → log and skip
  5. IF no PDFs found → log "No PDFs found"
  6. IF page blocked/CAPTCHA → log in scraping_issues_log.md, skip
  7. Update pdf_discovery_log.md with results
```

### Constraints

- **Protected paths**: Do NOT modify `01_knowledge_base/kb/` or `02_ingestion_pipeline/`
- **Flat folder structure**: All KB files go directly in category folders
- **PDFs in `pdfs/` subfolders**: e.g., `kb/01_regulatory/pdfs/`
- **Encoding**: UTF-8
- **Frontmatter**: Valid YAML, update `source_pdfs` field if PDF content merged
- **PDF relevance filter**: Only download freight/customs/trade PDFs. Skip annual reports, press releases, job postings
- **CAPTCHAs**: Log and skip — do NOT attempt to solve
- **Cookie banners**: Dismiss with privacy-preserving defaults (decline non-essential)
- **Resilience**: If a site is down/blocked, log it and move to the next URL. Do not retry more than once.

### Acceptance Criteria

- [ ] ALL ~70 source URLs visited via Chrome DevTools MCP
- [ ] `evaluate_script` PDF discovery run on each accessible page
- [ ] All discoverable relevant PDFs downloaded to `kb/<category>/pdfs/`
- [ ] `pdf_extractor.py` run on all downloaded PDFs
- [ ] Useful PDF content (HIGH/MEDIUM quality) merged into relevant KB docs
- [ ] `reports/pdf_discovery_log.md` updated with every URL visited and PDF found/not found
- [ ] `reports/scraping_issues_log.md` updated with any problems
- [ ] No files modified in `01_knowledge_base/kb/`

---

## Format

### PDF Discovery Log Format

```markdown
# PDF Discovery Log

**Date**: 2026-02-06
**Tool**: Chrome DevTools MCP
**Status**: In Progress

## Summary
| Category | URLs Visited | PDFs Found | PDFs Downloaded | PDFs Merged |
|----------|-------------|------------|-----------------|-------------|
| 6a Singapore Customs | 0/7 | 0 | 0 | 0 |
| 6b ASEAN Trade | 0/6 | 0 | 0 | 0 |
| 6c Country-specific | 0/14 | 0 | 0 | 0 |
| 6d Ocean Carriers | 0/13 | 0 | 0 | 0 |
| 6e Air Carriers | 0/9 | 0 | 0 | 0 |
| 6f Reference | 0/6 | 0 | 0 | 0 |
| **TOTAL** | **0/55** | **0** | **0** | **0** |

## 6a: Singapore Customs

### URL 1: https://www.customs.gov.sg/businesses/exporting-goods/overview/
- **Visited**: [timestamp]
- **Page loaded**: Yes/No
- **PDF links found**: [count]
  - [filename.pdf] ([pages], [quality]) → Merged into [doc] / Skipped ([reason])
- **Notes**: [any observations]
```

### Validation Commands

```bash
cd pilot_phase1_poc/04_retrieval_optimization
venv\Scripts\activate

# Count PDFs
python -c "from pathlib import Path; pdfs=list(Path('kb').rglob('*.pdf')); print(f'{len(pdfs)} PDFs downloaded')"

# Run pdf_extractor batch on all PDF folders
python scripts/pdf_extractor.py --batch kb/01_regulatory/pdfs/
python scripts/pdf_extractor.py --batch kb/02_carriers/pdfs/
python scripts/pdf_extractor.py --batch kb/03_reference/pdfs/

# Verify all docs still have valid frontmatter
python -c "
from scripts.process_docs import load_all_documents
docs = load_all_documents()
print(f'Loaded {len(docs)} documents')
"

# Quick ingestion test
python scripts/ingest.py --dry-run

# Verify no files in original KB were modified
git diff pilot_phase1_poc/01_knowledge_base/kb/
```

---

## Notes

- Pass 1 is already complete. This prompt covers ONLY Pass 2 (PDF discovery).
- Some government sites may block automated browsing or require CAPTCHA — log these and move on.
- PDF discovery is best-effort: not every URL will have PDFs, and not every PDF will be useful.
- For carrier sites, tariff/surcharge PDFs and service guides are highest-value targets.
- For government sites, procedure guides and classification documents are highest-value targets.
- Use `evaluate_script` for efficient PDF link extraction rather than visually scanning pages.
- Download PDFs via Bash (curl/PowerShell) rather than browser navigation for reliability.
