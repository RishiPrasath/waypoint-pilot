# Phase 2 Recommendations

**Date**: 2026-02-10
**Based on**: Phase 1 POC evaluation results (all 6 targets met)

---

## Priority Summary

| Priority | Count | Definition |
|----------|-------|------------|
| **P1** — Must-have | 5 | Required for production deployment or addresses critical POC gap |
| **P2** — Should-have | 5 | Significant user value or technical improvement |
| **P3** — Nice-to-have | 4 | Quality-of-life improvements, lower urgency |

---

## Features

- **P1 — Live system integration (TMS/WMS)**: Connect to shipment tracking, rate queries, and booking status APIs. These are the highest-volume CS queries and cannot be answered from a static KB. Addresses the single largest POC limitation.
- **P1 — Multi-turn conversation**: Add session memory so users can ask follow-up questions without restating context. POC treats every query as independent — "tell me more" or "what about Malaysia?" fail. Requires session storage and context carryover in the prompt.
- **P1 — Authentication and access control**: Add user sessions, role-based access, and API key management. POC API is completely open. Required before any deployment beyond internal testing.
- **P2 — Rate limiting and usage monitoring**: Track query volume, response times, and error rates per user/session. No observability exists in the POC — Groq API costs and abuse cannot be monitored.
- **P3 — Multi-language support**: CS agents handle queries in Mandarin, Malay, and Bahasa Indonesia. POC is English-only. Evaluate multilingual embedding models and LLM prompt translation.

## Knowledge Base

- **P1 — Expand to 80-100 documents**: POC's 30-doc KB has genuine content gaps (container specs, transit times, carrier routes, detailed ASEAN procedures). Target: double carrier coverage, add port-specific reference tables, deepen ASEAN regulatory docs for MY/ID/TH/VN/PH.
- **P2 — Dynamic content ingestion**: Add scheduled KB updates and incremental ingestion (currently requires `ingest.py --clear` full rebuild). Enable content team to add/update documents without developer intervention.
- **P2 — Structured data tables**: Add carrier route tables, port transit time matrices, and container specification reference docs. These are the top KB gaps identified in Round 2 failure analysis (4 KB Content Gap queries).
- **P3 — Content quality pipeline**: Add automated checks for frontmatter completeness, broken references, and stale content. POC relies on manual curation.

## Infrastructure

- **P1 — Production deployment**: Containerize (Docker), add health monitoring, configure auto-restart, and deploy to cloud. POC runs on a local development machine with manual startup.
- **P2 — Logging and analytics**: Add structured logging (query logs, retrieval scores, LLM token usage, response times) and a dashboard for monitoring system health and query patterns. POC has minimal console logging.
- **P3 — CI/CD pipeline**: Automate testing (217 tests across 3 frameworks) and deployment on git push. Currently all testing is manual.

## Model & Pipeline

- **P2 — Confidence score recalibration**: Current thresholds produce 86% Low, 14% Medium, 0% High. Analyze actual ChromaDB similarity score distribution and set thresholds that produce a meaningful distribution (e.g., 40% High, 40% Medium, 20% Low for in-scope queries).
- **P2 — Citation post-processing**: Add fuzzy title matching after LLM generation to catch citations that are semantically correct but don't match the exact `[Title > Section]` format. Addresses the Citation Gap failure mode (11 of 37 Round 2 failures).
- **P3 — LLM provider failover**: Add a secondary provider (e.g., OpenAI, Anthropic) for automatic failover when Groq is unavailable. POC depends on a single free-tier provider with no redundancy.
- **P3 — Embedding model evaluation**: Benchmark 2-3 alternatives (BGE-small, E5-small) against all-MiniLM-L6-v2. POC used ChromaDB's default without comparison. A 94% hit rate may improve with a better-suited model.
