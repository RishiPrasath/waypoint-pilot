# User Guide — Waypoint Co-Pilot

## What is Waypoint Co-Pilot?

Waypoint Co-Pilot is an AI-powered knowledge assistant for freight forwarding customer service agents. It answers questions about customs regulations, carrier services, booking procedures, and company policies for Singapore and Southeast Asia by searching a curated knowledge base of 30 documents and generating cited, structured responses.

The co-pilot is an **information tool** — it provides answers and references but cannot perform actions like booking shipments, tracking containers, or modifying orders.

## How to Use the System

1. Open the application at `http://localhost:5173` in your browser
2. Type your question in the input field
3. Press **Enter** or click the submit button
4. Review the response card (described below)

## How to Ask Effective Questions

**Be specific** — Include relevant details like country, carrier name, or document type.

| Less Effective | More Effective |
|----------------|---------------|
| "import docs" | "What documents are needed for importing electronics to Singapore?" |
| "carrier routes" | "What ocean routes does Maersk offer from Singapore?" |
| "customs rules" | "What are Singapore's rules of origin requirements for FTA benefits?" |
| "booking" | "What is the booking lead time for ocean freight shipments?" |

**Tips for best results:**
- Ask **one question at a time** — the system handles single queries, not follow-up conversations
- **Mention the country** when asking about regulations (e.g., "Singapore", "Malaysia", "ASEAN")
- **Name the carrier** when asking about specific services (e.g., "Maersk", "MSC", "ONE")
- **Use natural language** — no special syntax or commands needed
- **Include context** — "What GST applies to importing food products into Singapore?" is better than "GST rate?"

## Understanding the Response Card

Every response is displayed as a **4-section card**:

### 1. Answer

The main response to your question, formatted with:
- **Bold text** for key terms, thresholds, and deadlines
- **Numbered lists** for sequential steps or procedures
- **Bullet points** for non-sequential items
- **Headers** for multi-part answers
- **Inline citations** in `[Document Title]` or `[Document Title > Section]` format — these reference the source documents the answer is based on

Every factual claim should have a citation. If you see a statement without one, treat it with caution.

### 2. Sources

Clickable links to the **original external websites** that the answer draws from:
- Shows the document title, organization name, and domain
- Click to open the original regulatory page or carrier website
- Only appears for documents with public URLs (internal company documents won't show links)

### 3. Related Documents

**Category-colored chips** showing all knowledge base documents relevant to your query:

| Color | Category | Examples |
|-------|----------|----------|
| Blue | Regulatory | Singapore Customs procedures, ASEAN trade rules |
| Amber | Carrier | Maersk, MSC, ONE, PIL services |
| Green | Reference | Incoterms 2020, HS codes, FTA comparison |
| Gray | Internal | Booking procedures, SLA policy, escalation matrix |

Related documents include all retrieved documents, not just those directly cited in the answer. This helps you discover additional relevant material.

### 4. Confidence Footer

A **color-coded badge** indicating how well-supported the answer is:

| Badge | Level | Meaning | Action |
|-------|-------|---------|--------|
| Green | **High** | 3+ strong sources found | Answer is well-supported — use with confidence |
| Amber | **Medium** | 2+ sources with moderate relevance | Generally reliable — verify for critical decisions |
| Red | **Low** | Limited or weak sources | Treat as guidance only — confirm with a specialist |

The footer also displays:
- **Chunks retrieved** — number of knowledge base segments found
- **Chunks used** — number matched to citations in the answer
- **Response time** — how long the query took (typically ~1-2 seconds)

## When to Escalate

The co-pilot **cannot** help with the following — use the recommended channel instead:

| Request Type | What to Do |
|-------------|------------|
| Real-time shipment tracking | Use the tracking portal or contact operations |
| Live freight rate quotes | Contact the sales team for a quote |
| Booking modifications or cancellations | Contact your account manager or use the booking system |
| Account-specific data | Log into the customer portal or contact your account manager |
| Performing actions (book, cancel, track, order) | The co-pilot provides information only — use the appropriate system |
| Low-confidence answer on a critical question | Verify with a subject matter expert before acting |

If the co-pilot responds with "I don't have specific information about that topic," the question may be outside its knowledge base scope. Try rephrasing, or consult a colleague.

## Sample Queries

Here are example questions across different categories to help you get started:

### Regulatory Questions
1. **"What documents are needed to import goods into Singapore?"** — Returns import permit requirements, supporting documents, and customs procedures
2. **"What is the GST rate for imported goods in Singapore?"** — Returns current GST rate, exemptions, and relief schemes
3. **"What are Singapore's rules of origin requirements for FTA benefits?"** — Returns FTA rules, preferential tariff conditions

### Carrier Questions
4. **"What ocean routes does Maersk offer from Singapore?"** — Returns Maersk route network, transit times, and service names
5. **"What dangerous goods restrictions apply to air cargo?"** — Returns DG classification, packaging, and documentation requirements

### Reference Questions
6. **"What Incoterms 2020 terms are commonly used for sea freight?"** — Returns relevant Incoterms with responsibilities breakdown
7. **"How do I classify goods using HS codes?"** — Returns HS code structure, classification process, and resources

### Internal Policy Questions
8. **"What is the booking lead time for ocean freight?"** — Returns standard lead times and cut-off procedures
9. **"What are the SLA response times for customer inquiries?"** — Returns SLA tiers, response times, and escalation thresholds
10. **"What are the escalation procedures for urgent shipment issues?"** — Returns escalation matrix, contact points, and priority levels

## Related Documentation

- [Deployment Notes](deployment_notes.md) — How to install and run the system
- [Known Limitations](known_limitations.md) — What the system cannot do
- [API Contract](../architecture/api_contract.md) — Technical API specification
