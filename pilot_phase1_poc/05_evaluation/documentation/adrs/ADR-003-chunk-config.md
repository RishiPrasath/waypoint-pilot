# ADR-003: Chunking Configuration -- 600/90 with top_k=5

**Status**: Accepted
**Date**: 2025-02-02

## Context

The knowledge base contains 30 documents across 4 categories (regulatory, carrier, reference, internal procedures) in the freight forwarding domain. Documents contain structured content including:

- Regulatory tables (duty rates, permit types, thresholds)
- Carrier-specific details (routes, services, contact info)
- Abbreviation-heavy terminology (BL, FCL, LCL, SI, VGM, GST, HS)
- Step-by-step procedures with numbered lists

The chunking configuration directly impacts retrieval quality -- too large and context mixes across topics, too small and tables/lists fragment.

## Decision

Use **CHUNK_SIZE=600 characters** (~150 tokens), **CHUNK_OVERLAP=90 characters** (15%), and **top_k=5** retrieval results.

This configuration was confirmed optimal through systematic experimentation in Week 3, Task 8. The final knowledge base produces approximately 709 chunks from 30 documents.

## Alternatives Considered

All alternatives were tested against the same 50-query evaluation suite during Week 3 optimization:

| Configuration | Hit Rate | Delta | Observation |
|--------------|----------|-------|-------------|
| **600/90/top_k=5** (chosen) | **94%** | baseline | Best balance of precision and recall |
| 800/120/top_k=5 | 90% | -4% | Lost carrier-specific precision -- larger chunks mixed carrier info from different documents |
| 1000/150/top_k=5 | 86% | -8% | Too much content mixing -- regulatory and carrier content in same chunks |
| 400/60/top_k=5 | 88% | -6% | Tables fragmented across chunk boundaries, losing row-column relationships |
| 600/90/top_k=10 | 94% | +0% | More results did not help -- retrieval failures were caused by missing content, not insufficient result count |

### Key Insight

Content fixes (adding abbreviation tables, key terms sections to document bodies) produced +10 percentage points of improvement. Parameter tuning across 4 configurations produced 0 net improvement. For this KB size and domain, **content quality dominates over parameter tuning**.

Specific content fixes that improved hit rate:
1. Adding "Key Terms" body sections with abbreviation expansions (BL = Bill of Lading, etc.)
2. Adding FAQ-style content blocks to internal procedures

## Consequences

**Positive**:
- 94% raw hit rate (92% post-reclassification baseline, ~98% adjusted)
- Good precision for carrier-specific queries -- each carrier's content stays in its own chunks
- Tables remain intact within single chunks at 600 chars
- 15% overlap ensures cross-chunk continuity for multi-paragraph explanations
- top_k=5 provides enough context for LLM without overwhelming the prompt

**Negative**:
- Fixed configuration -- no adaptive chunking based on document type or content structure
- 600 chars is a hard limit that may split some longer regulatory tables
- Overlap creates minor content duplication (~15% storage overhead)
- Configuration is optimized for this specific 30-document KB; may not generalize to larger collections
- No sentence-boundary-aware splitting -- chunks may break mid-sentence
