# Waypoint Co-Pilot — Anticipated Q&A

**Prepared for**: Phase 1 POC Stakeholder Demo
**Date**: February 2026

---

## Cost & Budget

### Q1: What did the POC cost to build?
**A**: The POC infrastructure cost was $0 — ChromaDB and embeddings run locally, and the Groq LLM API free tier covered all 200+ queries across 4 evaluation rounds. The only cost was developer time over 4 weeks. Total LLM API spend for the entire POC was under $1. | Confidence: HIGH

### Q2: What will Phase 2 cost to run in production?
**A**: Primary costs will be cloud hosting ($50–150/month for a small VM or container), LLM API usage ($0.01–0.05 per query depending on provider and volume), and development effort (estimated 6–8 weeks for P1 features). At 500 queries/day, monthly LLM cost would be approximately $150–750 depending on the model chosen. ChromaDB remains free at this scale. | Confidence: MEDIUM

### Q3: What's the ROI / business case?
**A**: The POC demonstrated 87.2% query deflection — meaning 87% of in-scope questions were answered correctly without human intervention. If CS agents currently spend 15–20 minutes per query searching across PDFs and portals, even a 40% deflection rate (our minimum target) would save significant agent hours. At 100 queries/day with 87% deflection, that's roughly 87 queries resolved instantly vs. 15-minute manual searches. | Confidence: HIGH

---

## Architecture & Technology Choices

### Q4: Why ChromaDB over Pinecone or Weaviate?
**A**: ChromaDB was chosen for zero-configuration local operation — no API keys, no cloud account, no network dependency. For a 30-document POC, it provides sufficient performance (1.2s average query time including LLM). For Phase 2 production, we can evaluate managed alternatives (Pinecone, Weaviate Cloud) if we need distributed scaling or managed backups, but ChromaDB supports production deployments up to millions of documents. | Confidence: HIGH

### Q5: Why Groq with Llama 3.1 8B instead of OpenAI or Anthropic?
**A**: Groq offered a free tier sufficient for the entire POC evaluation (200+ queries, 4 rounds). Llama 3.1 8B Instant provided good instruction compliance for citation formatting and 1.2-second average response times. For Phase 2, we recommend adding LLM provider failover (P3 priority) so we can switch between Groq, OpenAI, and Anthropic based on availability and cost. The RAG architecture is LLM-agnostic — switching providers requires only a configuration change. | Confidence: HIGH

### Q6: Why a hybrid Python/Node.js architecture instead of one language?
**A**: Python has superior NLP library support (ChromaDB, langchain-text-splitters, ONNX embeddings) while Node.js excels at API servers and React integration. The subprocess bridge between them (JSON stdin/stdout) proved 100% reliable across 200+ queries with zero failures. This avoids forcing either language into a domain where it's weaker. | Confidence: HIGH

### Q7: Why local-first instead of cloud?
**A**: Local-first eliminated all infrastructure costs and cloud account dependencies during the POC. The entire system runs on a single developer machine — ChromaDB, embeddings, API server, and frontend. This also means no data leaves the local environment (important for sensitive freight/customs data). For production, we recommend Docker containerization (P1 priority) that can deploy to any cloud or on-premises server. | Confidence: HIGH

---

## Production Readiness

### Q8: What's needed to take this to production?
**A**: Five P1 items are required: (1) Docker containerization with health monitoring and auto-restart, (2) user authentication and role-based access control, (3) live TMS/WMS integration for real-time shipment data, (4) multi-turn conversation support, and (5) KB expansion to 80+ documents to cover content gaps. Estimated 6–8 weeks of development effort for all P1 items. | Confidence: MEDIUM

### Q9: How is sensitive data handled? What about PII?
**A**: Currently, the POC has no user authentication and no PII handling — it's designed for internal CS agent use only, answering questions about public regulations and internal policies. The knowledge base contains no customer data. For production, we need authentication (P1), audit logging (P2), and data handling policies. No customer PII flows through the RAG pipeline — queries are about procedures, not about specific shipments or customers. | Confidence: HIGH

### Q10: Can this be deployed on-premises vs. cloud?
**A**: Yes. The architecture is deployment-agnostic — ChromaDB and embeddings run locally, and the only external dependency is the LLM API call. For on-premises deployment, you could also use a local LLM (e.g., Ollama with Llama 3.1) to eliminate all external calls, though response quality and latency would need re-evaluation. Docker containerization (P1 priority) will support both cloud and on-prem deployment. | Confidence: MEDIUM

---

## Accuracy & Reliability

### Q11: How accurate is the system? Can we trust its answers?
**A**: The evaluation tested 50 queries across 5 categories with automated metrics. The system achieved 87.2% deflection rate (correctly answering in-scope queries), 96.0% citation accuracy (answers cite the correct source documents), and only 2.0% hallucination rate (and that single case was a measurement artifact, not actual hallucination). Every answer includes source citations so agents can verify before using the information. | Confidence: HIGH

### Q12: What happens when the system doesn't know the answer?
**A**: The system achieved 100% out-of-scope handling — all 11 OOS test queries (live tracking, rate quotes, booking requests) were correctly declined with responses like "I don't have specific information about that in my knowledge base." It never fabricates answers for topics outside its knowledge. The graceful decline mechanism uses a relevance threshold on retrieved chunks. | Confidence: HIGH

### Q13: How do we improve the 92% retrieval hit rate?
**A**: The primary path is KB expansion (P1 priority — from 30 to 80+ docs). The 8% miss rate comes from genuine content gaps: detailed container specifications, carrier-specific transit times, and port-specific procedures that aren't in the current KB. Our Week 3 analysis showed content additions were 5x more effective than parameter tuning for hit rate improvement. A secondary path is embedding model evaluation (P3) — benchmarking alternatives like BGE-small or E5-small against the current all-MiniLM-L6-v2. | Confidence: HIGH

### Q14: How reliable are the citations? Do they point to real sources?
**A**: 96% of citation-applicable queries correctly cited their source documents. Citations link to actual documents in the knowledge base with organization names and URLs (e.g., Singapore Customs, Maersk). The 4% gap was a single query where the LLM didn't format the citation in the expected pattern — the answer itself was correct, just the citation format was inconsistent. Citation fuzzy matching (P3 priority) would catch these format variations. | Confidence: HIGH

---

## Scaling

### Q15: Can the system handle 80+ documents? 200+?
**A**: ChromaDB handles millions of documents efficiently. The bottleneck is ingestion time and embedding quality, not storage. Scaling from 30 to 80 documents would increase chunks from ~709 to ~1,900 (proportionally). The key challenge at 200+ documents is maintaining retrieval precision — larger KBs may need category-based pre-filtering or hybrid search (keyword + semantic) to avoid irrelevant results diluting top-k results. | Confidence: MEDIUM

### Q16: Can it handle concurrent users?
**A**: The current Express API handles requests sequentially. For production concurrency, the main bottleneck is the LLM API call (~1.2s per query). ChromaDB supports concurrent reads natively. With a managed LLM provider and connection pooling, the system could handle 10–50 concurrent users without architectural changes. Beyond that, horizontal scaling (multiple API instances behind a load balancer) would be needed. | Confidence: MEDIUM

### Q17: What about multi-language support (Mandarin, Malay, Bahasa)?
**A**: The POC is English-only. Adding multi-language support (P3 priority) requires three changes: (1) a multilingual embedding model (e.g., multilingual-MiniLM or BGE-M3), (2) LLM prompt translation to handle queries in other languages, and (3) multilingual KB content or cross-lingual retrieval. This is a significant effort — estimated 2–3 weeks — but the architecture supports it without fundamental changes. | Confidence: LOW

---

## Integration

### Q18: How would TMS/WMS live data integration work?
**A**: The RAG pipeline already has a context assembly step where retrieved KB chunks are packaged for the LLM. Live data integration (P1 priority) would add a parallel data source: when the query mentions a specific shipment, booking, or tracking number, the system calls the TMS/WMS API, formats the result, and includes it alongside KB chunks in the LLM context. The LLM then synthesizes both static knowledge and live data into a single response. | Confidence: MEDIUM

### Q19: How do we add new documents to the knowledge base?
**A**: Currently, adding a document requires: (1) create a Markdown file with YAML frontmatter in the `kb/` directory, (2) run `python scripts/ingest.py --clear` to rebuild the entire vector store (~30 seconds for 30 docs). For Phase 2, dynamic ingestion (P2 priority) would enable incremental updates — add a document without rebuilding the entire index — and a content management interface so non-developers can contribute. | Confidence: HIGH

### Q20: Can it integrate with Zendesk, Freshdesk, or other CS platforms?
**A**: The system exposes a standard REST API (`POST /api/query`) that returns structured JSON (answer, sources, relatedDocs, confidence). Any CS platform with webhook or API integration capability can call this endpoint. A typical integration would embed the co-pilot as a sidebar widget in the agent's ticket view, pre-populating the query from the customer's question. This is a frontend integration task, not a backend change. | Confidence: MEDIUM
