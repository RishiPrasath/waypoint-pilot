# Waypoint Phase 1 POC: Pilot Overview

**Project**: Waypoint — Guided Intelligence for Customer Service  
**Company**: CYAIRE (AI Solution Engineering, Singapore)  
**Pilot Duration**: 30 days  
**Target Segment**: 3PL / Freight Forwarding  
**End User**: Customer Service Agents (Co-Pilot)

---

## Executive Summary

This pilot validates whether a RAG-based co-pilot can meaningfully assist customer service agents in a freight forwarding context by providing instant, accurate answers from a curated knowledge base.

### Core Hypothesis

> Customer service agents spend significant time searching for information across fragmented sources. A co-pilot that retrieves relevant context from shipping documentation, customs regulations, and carrier policies can reduce response time and improve accuracy.

### Pilot Approach

- **Phase 1 Focus**: Knowledge-base-only queries (no live system integration)
- **Knowledge Sources**: Public regulatory docs + synthetic internal policies + public carrier information
- **Deployment**: Local development → Single-user testing
- **Success Threshold**: 40% of test queries answered accurately without human escalation

---

## Document Index

| Document | Description | Status |
|----------|-------------|--------|
| [01 - Scope Definition](./01_scope_definition.md) | What's in/out, constraints, success criteria | ✅ |
| [02 - Use Case Catalog](./02_use_cases.md) | CS agent scenarios for freight forwarding | ✅ |
| [03 - Knowledge Base Blueprint](./03_knowledge_base_blueprint.md) | Public sources + synthetic doc templates | ✅ |
| [04 - Technical Architecture](./04_technical_architecture.md) | Free/low-cost stack recommendations | ✅ |
| [05 - Execution Roadmap](./05_execution_roadmap.md) | 30-day week-by-week milestones | ✅ |
| [06 - Evaluation Framework](./06_evaluation_framework.md) | Metrics, testing, go/no-go criteria | ✅ |

---

## Key Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Timeline | 30 days | Aggressive but achievable for focused POC |
| Team Size | 1 (solo dev) | Constrains scope; favors simplicity |
| Budget | Minimal (free tools preferred) | Use open-source, free tiers, local dev |
| Geographic Focus | Singapore-centric | Simplifies regulatory scope for POC |
| Primary Domain | Freight Forwarding | Highest complexity, highest value |
| Secondary Scope | COD, SLA, Service Scope | If time permits |

---

## Tech Stack Summary

| Component | Tool | Cost |
|-----------|------|------|
| Vector Database | ChromaDB (local dev) | Free |
| LLM | Groq API (Llama 3) or Claude Haiku | ~$0.05-0.25/1M tokens |
| Embedding | sentence-transformers (local) or Voyage AI free tier | Free |
| Backend | Node.js | Free |
| UI | Simple web interface (HTML/JS) or CLI | Free |
| Document Processing | LangChain / LlamaIndex | Free |

---

## Risk Factors

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Knowledge base too thin | High | Start with 20-30 quality docs; expand iteratively |
| Hallucination on edge cases | Medium | Implement confidence scoring; default to "I don't know" |
| Scope creep | High | Strict adherence to Phase 1 boundaries |
| Solo dev bottleneck | Medium | Prioritize ruthlessly; cut features not quality |

---

## Quick Links

**Immediate Next Steps** → [05 - Execution Roadmap](./05_execution_roadmap.md)  
**What to Build First** → [02 - Use Cases](./02_use_cases.md) (prioritized list)  
**Tech Decisions** → [04 - Technical Architecture](./04_technical_architecture.md)

---

*Last Updated: January 2025*  
*Version: 1.0*
