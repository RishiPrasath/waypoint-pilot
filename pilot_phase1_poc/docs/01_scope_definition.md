# 01 - Scope Definition

**Document Type**: Scope Statement  
**Pilot**: Waypoint Phase 1 POC  
**Version**: 1.0

---

## Pilot Objective

Demonstrate that a RAG-based co-pilot can provide accurate, source-cited answers to common freight forwarding customer service queries using a curated knowledge base of regulatory documents, carrier information, and synthetic internal policies.

---

## In Scope

### Primary Domain: Freight Forwarding

| Category | Description | Example Queries |
|----------|-------------|-----------------|
| **Shipment Booking** | Booking procedures, documentation requirements, lead times | "What documents are needed for an LCL shipment to Jakarta?" |
| **Customs & Documentation** | HS codes, duties, import/export requirements, certificates | "What's the GST treatment for goods in Singapore FTZ?" |
| **Carrier Selection Guidance** | Carrier capabilities, transit times, service comparisons | "Which carriers offer direct sailing to Ho Chi Minh?" |

### Secondary Scope (If Time Permits)

| Category | Description | Priority |
|----------|-------------|----------|
| **COD Procedures** | Cash-on-delivery workflows, reconciliation | P2 |
| **SLA Inquiries** | Service level terms, penalty structures | P2 |
| **Service Scope Clarification** | What's included/excluded in service offerings | P3 |

### Geographic Focus

- **Primary**: Singapore (origin/destination)
- **Secondary**: Malaysia, Indonesia, Thailand, Vietnam, Philippines
- **Rationale**: Singapore-centric simplifies regulatory complexity while allowing regional relevance

### Carriers in Scope

**Ocean Freight**
- PIL (Pacific International Lines) — Regional specialist
- Maersk — Global, strong SEA presence
- ONE (Ocean Network Express) — Major Asia routes
- Evergreen — Significant intra-Asia coverage

**Air Freight**
- Singapore Airlines Cargo
- Cathay Cargo

**Regional/Last-Mile** (for secondary scope)
- Ninja Van
- J&T Express
- Kerry Logistics

---

## Out of Scope

### Explicitly Excluded from Phase 1

| Exclusion | Reason |
|-----------|--------|
| Live TMS/WMS integration | Requires system access; Phase 2+ |
| Real-time tracking queries | Needs API integration |
| Actual booking execution | Transaction processing out of scope |
| Rate quotations | Requires live rate data |
| Claims processing | Complex multi-step workflow; Phase 3 |
| Hazmat/DG shipments | High complexity, high risk |
| Multi-country regulatory comparison | Scope creep risk; Singapore-first |
| B2C end-consumer interface | Focus is CS agent co-pilot |

### Technical Exclusions

| Exclusion | Reason |
|-----------|--------|
| Production deployment | POC is local development only |
| User authentication | Single-user testing |
| Multi-tenancy | Not needed for POC |
| Conversation history persistence | Nice-to-have, not essential |
| Advanced guardrails | Basic confidence scoring only |

---

## Constraints

### Timeline
- **Total Duration**: 30 days
- **Working Assumption**: Full-time equivalent effort
- **Buffer**: None (aggressive timeline)

### Resources
- **Team**: 1 developer (solo)
- **Budget**: Minimal; free tools preferred
- **Infrastructure**: Local development machine

### Technical Constraints
- Must work offline/locally for development
- LLM API calls should be cost-efficient (< $10 total for POC)
- No enterprise software dependencies

### Knowledge Base Constraints
- Public documents only (no proprietary client data)
- Synthetic documents for internal policies
- English language only

---

## Success Criteria

### Primary Metric

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Query Deflection Rate** | 40% | % of test queries answered accurately without needing human escalation |

### Supporting Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Citation Accuracy** | 80% | Responses include correct source attribution |
| **Hallucination Rate** | < 15% | Responses containing fabricated information |
| **"I Don't Know" Appropriateness** | 90% | System correctly declines out-of-scope queries |
| **Response Latency** | < 5 seconds | Time from query to response |

### Qualitative Success Indicators
- CS agent (simulated) finds responses useful
- Responses are appropriately scoped (not over-promising)
- System gracefully handles edge cases
- Knowledge base is maintainable/extendable

---

## Assumptions

| Assumption | Risk if Invalid |
|------------|-----------------|
| Public regulatory docs are sufficient for customs queries | May need to purchase/access proprietary sources |
| Synthetic internal docs are realistic enough | Real client validation needed post-POC |
| 20-30 documents provide adequate coverage | May need more docs for 40% deflection |
| Free LLM tier is sufficient for testing | May need small API budget |
| Single-market focus (Singapore) is acceptable | May limit demo appeal |

---

## Stakeholders

| Role | Person/Entity | Interest |
|------|---------------|----------|
| Developer | Rishi | Build and validate POC |
| Sponsor | CYAIRE | Evaluate market viability |
| Future User | 3PL CS Agents | End-user validation (simulated in POC) |
| Future Customer | 3PL Companies | Commercial opportunity |

---

## Definition of Done (POC Complete)

- [ ] Knowledge base populated with 20-30 curated documents
- [ ] RAG pipeline functional (embed → retrieve → generate)
- [ ] 50 test queries executed with documented results
- [ ] Deflection rate calculated and reported
- [ ] Architecture documented for Phase 2 extension
- [ ] Demo-ready for CYAIRE internal review

---

## Change Control

Given the 30-day timeline, scope changes should be:
1. **Avoided** unless critical blocker discovered
2. **Traded** — add something = remove something else
3. **Documented** — any changes logged with rationale

---

*Next Document*: [02 - Use Case Catalog](./02_use_cases.md)
