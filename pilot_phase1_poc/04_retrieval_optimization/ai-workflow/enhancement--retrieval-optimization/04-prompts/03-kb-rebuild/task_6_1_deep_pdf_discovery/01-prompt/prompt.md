# Task 6.1: Deep PDF Discovery (Bonus)

## Persona
You are a knowledge base enrichment specialist performing a **second-pass deep crawl** of source websites. Task 6 did a flat scan (checking each URL for `a[href*=".pdf"]`). This task goes deeper — clicking into sub-sections, expanding accordions, and following keyword-rich internal links to uncover PDFs buried 1-2 levels below the surface.

## Context

### What Task 6 Did (Flat Scan)
- Visited 55 top-level URLs
- Scanned each page for direct PDF links via `document.querySelectorAll('a[href*=".pdf"]')`
- Downloaded 25 PDFs, merged content into 5 KB docs
- **Did NOT**: click into sub-pages, expand accordions, follow "Key Documents" links, or navigate to related pages

### What Task 6.1 Does (Deep Crawl)
- Revisit the **highest-yield sites** from Task 6 (those that had PDFs or keyword-rich sub-pages)
- On each page, identify and follow **keyword-rich internal links** likely to contain more documents
- Expand accordions/tabs to reveal hidden PDF links
- Follow sub-pages 1-2 levels deep
- Apply the same download → extract → evaluate → merge workflow from Task 6

### Why This Matters
The ASEAN Trade in Goods page alone has 68 PDF links on the surface, but also has:
- "Key Documents" accordion section (collapsed, not scanned)
- "Relevant Documents" accordion section (collapsed, not scanned)
- Sub-pages: "Trade Facilitation", "Rules of Origin", "AFTA Publications" (never visited)
- Deep links: "Annex 2 (Tariff Schedules)", framework agreements (never followed)

Similar patterns likely exist on Singapore Customs, Maersk, and WCO sites.

## Task

### Strategy: Keyword-Driven Deep Crawl

**Step 1: Identify Target Keywords for Link Discovery**

Use these keyword categories to find clickable elements that lead to documents:

| Category | Keywords |
|----------|----------|
| **Document sections** | key documents, relevant documents, downloads, resources, publications, library, repository |
| **Regulatory content** | guidelines, handbook, manual, circular, notice, regulation, directive, advisory |
| **Forms & templates** | forms, templates, application, declaration, certificate |
| **Legal instruments** | agreement, protocol, annex, appendix, amendment, schedule, framework |
| **Trade-specific** | tariff, rules of origin, customs, facilitation, procedures, compliance |
| **Navigation cues** | read more, view all, see more, learn more, full list, related, explore |

**Step 2: JavaScript Discovery Script (Enhanced)**

Use this enhanced script on each page to find both PDFs and keyword-rich sub-links:

```javascript
() => {
  const docKeywords = [
    'document', 'download', 'resource', 'publication', 'guideline', 'guide',
    'form', 'template', 'annex', 'protocol', 'agreement', 'handbook', 'manual',
    'report', 'circular', 'regulation', 'rule', 'schedule', 'tariff', 'origin',
    'facilitation', 'customs', 'procedure', 'framework', 'appendix', 'read more',
    'view all', 'see more', 'learn more', 'full list', 'library', 'notice',
    'advisory', 'directive', 'certificate', 'declaration', 'compliance'
  ];

  const allLinks = Array.from(document.querySelectorAll('a'));
  const pdfs = [];
  const deepLinks = [];
  const seen = new Set();

  allLinks.forEach(a => {
    const text = a.textContent.trim().toLowerCase();
    const href = a.href || '';
    if (!href || href.startsWith('javascript') || seen.has(href)) return;
    seen.add(href);

    if (href.includes('.pdf')) {
      pdfs.push({ text: a.textContent.trim().substring(0, 120), href });
    } else if (text.length > 5 && text.length < 200) {
      const matched = docKeywords.filter(k => text.includes(k) || href.toLowerCase().includes(k));
      if (matched.length > 0) {
        deepLinks.push({ text: text.substring(0, 120), href, keywords: matched });
      }
    }
  });

  // Check for accordions/expandable sections
  const expandables = document.querySelectorAll('[aria-expanded="false"], .accordion-button:not(.show), details:not([open])');

  return {
    pageTitle: document.title,
    url: window.location.href,
    pdfCount: pdfs.length,
    pdfs: pdfs.slice(0, 20),
    deepLinkCount: deepLinks.length,
    deepLinks: deepLinks.slice(0, 20),
    collapsedSections: expandables.length
  };
}
```

**Step 3: Accordion/Tab Expansion**

When collapsed sections are found:
```javascript
() => {
  // Click all accordion headers to expand
  const expandables = document.querySelectorAll('[aria-expanded="false"]');
  expandables.forEach(el => el.click());
  return { expanded: expandables.length };
}
```

Then re-run the discovery script to find newly revealed PDFs.

### Sites to Deep Crawl (Priority Order)

**Tier 1 — High Yield (had PDFs + sub-pages)**

| Site | Reason | Deep Crawl Targets |
|------|--------|--------------------|
| **asean.org** (ASEAN) | 68 PDFs on surface + accordion sections + sub-pages | Key Documents accordion, Relevant Documents accordion, "Trade Facilitation" sub-page, "Rules of Origin" sub-page, "AFTA Publications" sub-page |
| **customs.gov.sg** (SG Customs) | 7 PDFs found, but site has deep navigation | Look for "Forms & Guides" sections, "E-Services" sub-pages, related topic sidebars |
| **maersk.com/local-information** | 19 PDFs on Singapore page | Check if other Asia-Pacific country pages exist, look for "Resources" or "Downloads" sections |

**Tier 2 — Moderate Potential (had useful content but few PDFs)**

| Site | Reason | Deep Crawl Targets |
|------|--------|--------------------|
| **wcoomd.org** | 2 PDFs found, large document repository | "Publications" section, "Activities and Programmes", "Resources" |
| **siacargo.com** | 2 PDFs found, product pages | "Resources", "Downloads" in product sub-pages |

**Tier 3 — Low Potential (skip unless time allows)**

| Site | Reason |
|------|--------|
| Country customs portals | Web apps with no PDFs in Task 6 |
| ICC/iccwbo.org | Content behind paywall |
| PIL, ONE, Evergreen | No relevant PDFs in Task 6 |

### Workflow Per Site

1. **Navigate** to the site's main page using `navigate_page`
2. **Run enhanced discovery script** via `evaluate_script`
3. **Expand accordions** if collapsed sections found
4. **Re-scan** for newly revealed PDFs
5. **Follow keyword-rich sub-links** (max 2 levels deep per site)
6. **On each sub-page**: run discovery script, download new PDFs
7. **Download** new PDFs via `curl` (with User-Agent header)
8. **Extract** via `pdf_extractor.py`
9. **Evaluate** quality (HIGH/MEDIUM/LOW) — only merge HIGH
10. **Merge** useful content into existing KB docs OR create new standalone extracts
11. **Log** all findings to `reports/deep_pdf_discovery_log.md`

### Download & Merge Rules

- Only download PDFs that appear **relevant** to the KB scope (Singapore trade, ASEAN customs, carrier operations)
- Skip: sailing schedules, India-specific tariffs, ITA boilerplate, login/registration forms
- Use `curl -L -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"` for all downloads
- Extract with: `venv/Scripts/python scripts/pdf_extractor.py <path>`
- Only merge HIGH quality extracts that address known failing queries or fill content gaps
- For large PDFs (>50 pages): reference in frontmatter only, don't merge

### Tool Mapping

| Action | Tool |
|--------|------|
| Navigate to URL | `mcp__chrome-devtools__navigate_page` |
| Scan for PDFs + deep links | `mcp__chrome-devtools__evaluate_script` |
| Expand accordions | `mcp__chrome-devtools__evaluate_script` |
| Click into sub-sections | `mcp__chrome-devtools__click` |
| Take page snapshot | `mcp__chrome-devtools__take_snapshot` |
| Screenshot for reference | `mcp__chrome-devtools__take_screenshot` |
| Download PDF | `Bash` (curl) |
| Extract PDF | `Bash` (pdf_extractor.py) |
| Merge content | `Edit` |
| Update frontmatter | `Edit` |

## Format

### Output Files
- `reports/deep_pdf_discovery_log.md` — Detailed log of all deep crawl findings
- `02-output/REPORT.md` — Summary report with stats and recommendations

### Discovery Log Format
```markdown
## [Site Name]

### Page: [URL]
- **Deep links found**: N
- **Accordions expanded**: N
- **New PDFs discovered**: N
  - filename.pdf (pages, quality) → Action taken

### Sub-page: [URL] (followed from [parent link text])
- **PDFs found**: N
  - filename.pdf (pages, quality) → Action taken
```

### Success Criteria
- All Tier 1 sites deep-crawled
- All accordions expanded and scanned
- All keyword-rich sub-links followed (1-2 levels)
- New PDFs downloaded, extracted, and evaluated
- Useful content merged into KB docs
- Complete log in `reports/deep_pdf_discovery_log.md`
