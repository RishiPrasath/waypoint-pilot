# ADR-006: Response UX Design -- 4-Section Card Layout

**Status**: Accepted
**Date**: 2025-02-06

## Context

Customer service agents at freight forwarding companies need quick, actionable answers when handling shipment inquiries. The response format must:

- Present all relevant information without requiring scrolling or tab switching
- Build trust through visible source attribution and confidence indicators
- Enable quick navigation to related knowledge base documents
- Distinguish between external regulatory sources and internal procedures
- Support markdown formatting for structured content (tables, lists, bold)

This decision was made during Week 4 (Task T1.1 UX Redesign) as part of the evaluation and documentation phase.

## Decision

Use a **4-section card layout** for all query responses:

### Section 1: Answer
- Rendered as markdown (headings, bold, lists, tables)
- Contains inline citation markers in `[Document Title > Section Name]` format
- Fills the full card width as the primary content area

### Section 2: Sources
- External URLs from cited documents
- Each source shows: title, organization name, clickable URL, section reference
- Only populated when citations match documents with external `source_urls`
- Empty for queries answered entirely from internal documents

### Section 3: Related Documents
- Category-colored chips for each retrieved knowledge base document
- Categories: `regulatory` (blue), `carrier` (green), `reference` (purple), `internal` (orange)
- Each chip shows document title and category label
- Includes all retrieved documents, not just cited ones

### Section 4: Confidence Footer
- Confidence level badge: `High` (green), `Medium` (amber), `Low` (red)
- Metadata stats: chunks retrieved, chunks used, latency in milliseconds, model name
- Displayed as a compact footer bar below the main content

## Alternatives Considered

| Alternative | Reason for Rejection |
|------------|---------------------|
| **Single text block** | Poor scannability. Sources and confidence mixed into prose text. Customer service agents need to quickly assess answer reliability -- a wall of text makes this difficult. |
| **Chat-style conversation** | Adds complex state management (message history, context window). Overkill for a POC where each query is independent. Would require session persistence and conversation threading. |
| **Tabbed view** | Hides information behind tabs. Agents would need to click between "Answer", "Sources", and "Details" tabs. Key information (confidence level, source attribution) should be visible immediately. |
| **Accordion/collapsible sections** | Requires clicks to expand sections. Similar problem to tabs -- important information starts hidden. Agents need all context at a glance. |

## Consequences

**Positive**:
- All information visible without scrolling on standard desktop viewport
- Confidence badge and source attribution build agent trust in AI-generated answers
- Category chips in Related Documents section aid navigation to source material
- Clean visual hierarchy: answer (largest), sources, related docs, confidence (smallest)
- Markdown rendering supports tables and lists common in freight forwarding content (duty rates, document checklists)

**Negative**:
- Fixed layout -- no customization for different query types or user preferences
- No conversation history -- each query/response is standalone with no context from previous interactions
- Sources section appears empty for queries answered entirely from internal/synthetic documents (may confuse agents expecting external links)
- Card layout optimized for desktop viewport; may need responsive adjustments for mobile or narrow screens
- No inline feedback mechanism (thumbs up/down) for response quality -- would need to be added separately
