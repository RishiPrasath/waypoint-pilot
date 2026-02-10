# Known Limitations — Waypoint Co-Pilot (Phase 1 POC)

This document sets honest expectations about what the POC can and cannot do. These are known constraints, not bugs — many are intentional scoping decisions for a Phase 1 proof-of-concept.

## Scope Limitations

These are **by design** for the POC and would be addressed in a production system:

| Limitation | Impact | Production Path |
|-----------|--------|-----------------|
| **No live system integration** | Cannot connect to TMS, WMS, tracking, or booking platforms | Integrate via APIs in Phase 2 |
| **No real-time data** | Cannot provide live freight rates, shipment status, or inventory levels | Add real-time data feeds |
| **No multi-turn conversation** | Each query is independent — no session memory or follow-up context | Add conversation history with session management |
| **No authentication or authorization** | No user accounts, roles, or access control | Add SSO/LDAP integration |
| **No audit trail** | Queries and responses are not logged or persisted | Add query logging and analytics |
| **Singapore-centric** | Regulatory content focuses on Singapore Customs; limited SEA secondary coverage | Expand KB for Malaysia, Indonesia, Thailand, etc. |
| **English only** | No multilingual support | Add language detection and translation |
| **Single-user design** | Local deployment, no concurrent user support | Deploy with managed infrastructure |

## Technical Limitations

| Limitation | Detail | Mitigation |
|-----------|--------|------------|
| **Single LLM (no fallback)** | Uses only Llama 3.1 8B via Groq API — if Groq is down, the pipeline fails | Add fallback LLM (e.g., OpenAI GPT-4o-mini) |
| **Groq free tier rate limits** | ~30 requests/minute on free tier — not suitable for production load | Upgrade to paid Groq tier or switch provider |
| **Python subprocess per query** | Each query spawns a new Python process for ChromaDB — adds ~200ms latency | Use native ChromaDB JS client or persistent Python server |
| **Local ChromaDB only** | File-based vector store on single machine — no replication or scaling | Migrate to managed vector DB (Pinecone, Weaviate Cloud) |
| **No response caching** | Identical queries re-run the full pipeline every time | Add query cache with TTL |
| **No streaming** | Full response generated before display (typically ~1.0-1.5s) | Add streaming support for progressive rendering |
| **Max 500 output tokens** | Very detailed answers may be truncated by the token limit | Increase limit or add pagination |
| **No request queuing** | Under load, all requests hit the LLM simultaneously | Add request queue with concurrency limits |

## Knowledge Base Limitations

| Limitation | Detail |
|-----------|--------|
| **Static content** | Documents are point-in-time snapshots (last updated dates vary from 2024-2025). Regulations, carrier routes, and policies change — content is not auto-updated. |
| **30 documents / 709 chunks** | Limited breadth. Some niche freight forwarding topics may not be covered. |
| **92% retrieval hit rate** | In the 50-query test suite, ~4 queries did not find relevant chunks. Edge cases and unusual phrasing may miss. |
| **Frontmatter not embedded** | `retrieval_keywords` in YAML frontmatter are stored as metadata but not embedded. If a key term only appears in frontmatter (not body text), it won't be found via semantic search. |
| **Abbreviation sensitivity** | Queries using abbreviations (e.g., "BL", "FCL", "LCL") may miss if the abbreviation isn't in the document body. Key abbreviation tables were added during Week 3 optimization but coverage isn't exhaustive. |
| **PDF content partially captured** | Regulatory PDFs were selectively merged into markdown docs. Some detailed annexes, schedules, and appendices were not fully extracted. |

## Evaluation Results (Round 4)

Final evaluation results from the 50-query automated test suite:

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Deflection Rate | 87.2% | ≥ 40% | PASS |
| Citation Accuracy (adjusted) | 96.0% | ≥ 80% | PASS |
| Citation Accuracy (raw) | 97.4% | — | Reference |
| Hallucination Rate | 2.0%* | < 15% | PASS |
| OOS Handling | 100.0% | ≥ 90% | PASS |
| Avg Latency | 1182ms | < 5s | PASS |
| System Stability | No crashes | No crashes | PASS |

*The 2.0% hallucination rate is a measurement artifact — Q-39 ("standard liability") retrieved 0 chunks and correctly declined, but the baseline's `must_not_contain` check flagged the decline message. This is not actual hallucination.

### Evaluation Gaps

- **Citation accuracy measurement**: The `applicable` flag was added to distinguish queries where citation is possible (chunks retrieved) from queries where it isn't (0 chunks → N/A). 14 of 39 in-scope queries were marked N/A. The 96.0% rate is calculated on the 25 applicable queries.
- **Confidence distribution skew**: 43/50 queries received "Low" confidence, 7 received "Medium", 0 received "High". The confidence thresholds were lowered during Phase 3 (High: 0.6→0.5, Medium: 0.4→0.3) but most queries still score Low because ChromaDB similarity scores tend to be in the 0.15-0.45 range for this embedding model and KB size.
- **LLM nondeterminism**: At temperature 0.3, the LLM produces slightly different responses across runs. Three citation failures in Round 3 (Q-03, Q-23, Q-29) self-resolved in Round 4 without code changes — the LLM happened to cite correctly.
- **Carrier-specific gaps**: Some carrier questions return general freight industry answers rather than carrier-specific details. The 6 carrier documents cover major services but not all routes and schedules.
- **SLA category hallucination**: 1/10 SLA queries (10%) triggered a false hallucination flag — the highest per-category rate. Internal policy documents may need more explicit coverage.

## Out-of-Scope Query Categories

The system is designed to politely decline and redirect these requests:

| Category | System Response | User Should |
|----------|----------------|-------------|
| Real-time tracking | "For shipment tracking, please use our tracking portal..." | Use tracking portal or contact operations |
| Live freight rates | "Freight rates vary by route and timing..." | Contact sales team |
| Booking changes | "To modify a booking, please contact..." | Contact account manager or booking system |
| Account-specific data | "For account-specific information..." | Customer portal or account manager |
| Action requests (book, cancel, track, modify) | "I cannot [action] on your behalf..." | Use appropriate system or contact team |

## Recommendations for Phase 2

Based on POC findings, the following improvements are recommended for a production system:

1. **LLM fallback chain** — Add OpenAI GPT-4o-mini or Anthropic Claude as backup when Groq is unavailable
2. **Query caching** — Cache responses for identical or semantically similar queries (Redis or in-memory)
3. **Authentication and logging** — Add user authentication (SSO/LDAP) and persist all queries for analytics
4. **Managed vector database** — Migrate from local ChromaDB to Pinecone or Weaviate Cloud for scalability
5. **KB content pipeline** — Schedule regular content refreshes from regulatory sources; consider automated PDF extraction
6. **Multi-turn conversations** — Add session context so users can ask follow-up questions
7. **Streaming responses** — Stream LLM output for better perceived latency
8. **Confidence calibration** — Investigate alternative scoring methods (e.g., cross-encoder reranking) to improve confidence distribution
9. **Multilingual support** — Add language detection and translation for SEA markets
10. **Native ChromaDB client** — Replace Python subprocess bridge with direct JS integration to eliminate ~200ms overhead

## Related Documentation

- [User Guide](user_guide.md) — How CS agents use the system
- [Deployment Notes](deployment_notes.md) — Installation and setup
- [System Overview](../architecture/system_overview.md) — Architecture and tech stack
- [RAG Pipeline Flow](../architecture/rag_pipeline_flow.md) — Pipeline stage details
