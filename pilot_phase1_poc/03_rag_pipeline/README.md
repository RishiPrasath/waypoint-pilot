# Waypoint RAG Pipeline

A retrieval-augmented generation (RAG) system for freight forwarding customer service. Built for Waypoint, a Singapore-based 3PL company serving Southeast Asia.

## Features

- **Knowledge-Based Answers**: Retrieves relevant information from 29 curated documents (~350 chunks)
- **Source Citations**: Every response includes document citations with links
- **Confidence Indicators**: High/Medium/Low confidence based on retrieval quality
- **Out-of-Scope Detection**: Gracefully declines questions outside knowledge base
- **Action Request Handling**: Detects and redirects booking/tracking requests
- **Fast Responses**: Average latency ~2-4 seconds

## Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Vector Database | ChromaDB | 0.5.23 |
| Embeddings | all-MiniLM-L6-v2 | ONNX |
| Backend | Node.js + Express | 18+ |
| Frontend | React + Tailwind | 18+ |
| LLM | Groq (Llama 3.1 8B) | - |

---

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Groq API key ([Get one here](https://console.groq.com))

### Installation

```bash
# Clone and navigate to RAG pipeline
cd pilot_phase1_poc/03_rag_pipeline

# Install backend dependencies
npm install

# Install frontend dependencies
cd client && npm install && cd ..

# Create environment file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Running the Application

```bash
# Terminal 1: Start backend
npm start
# API available at http://localhost:3000

# Terminal 2: Start frontend
cd client && npm run dev
# UI available at http://localhost:5173
```

### Quick Test

```bash
# Health check
curl http://localhost:3000/api/health

# Query test
curl -X POST http://localhost:3000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the GST rate in Singapore?"}'
```

---

## Architecture

### System Overview

```
┌─────────────┐     ┌─────────────────────────────────────────────┐
│   React UI  │────▶│              Express API                    │
│  (Port 5173)│     │              (Port 3000)                    │
└─────────────┘     └─────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
              ┌──────────┐     ┌──────────┐     ┌──────────┐
              │ Retrieval│     │   LLM    │     │ Citation │
              │ Service  │     │ Service  │     │ Extractor│
              └────┬─────┘     └────┬─────┘     └──────────┘
                   │                │
                   ▼                ▼
              ┌──────────┐     ┌──────────┐
              │ ChromaDB │     │ Groq API │
              │ (Local)  │     │ (Cloud)  │
              └──────────┘     └──────────┘
```

### Data Flow

1. **Query Input**: User submits question via UI or API
2. **Retrieval**: Query embedded and matched against ChromaDB (top-5 chunks)
3. **Context Assembly**: Relevant chunks formatted with metadata
4. **Generation**: Groq LLM generates response with citations
5. **Citation Extraction**: Citations parsed and matched to sources
6. **Response**: Answer returned with citations, confidence, and metadata

### Key Components

| Component | File | Purpose |
|-----------|------|---------|
| Pipeline Orchestrator | `src/services/pipeline.js` | Coordinates RAG flow |
| Retrieval Service | `src/services/retrieval.js` | ChromaDB queries |
| LLM Service | `src/services/llm.js` | Groq API integration |
| Citation Extractor | `src/services/citations.js` | Parses citations |
| System Prompt | `src/prompts/system.txt` | LLM instructions |

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | API server port |
| `GROQ_API_KEY` | - | **Required**: Groq API key |
| `GROQ_MODEL` | llama-3.1-8b-instant | LLM model |
| `CHROMA_PATH` | ./chroma_data | Vector database path |
| `COLLECTION_NAME` | waypoint_kb | ChromaDB collection |
| `LOG_LEVEL` | info | Logging: debug/info/warn/error |

### Retrieval Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `RETRIEVAL_TOP_K` | 5 | Chunks to retrieve |
| `RELEVANCE_THRESHOLD` | 0.3 | Minimum similarity score |
| `MAX_CONTEXT_CHARS` | 4000 | Context size limit |

---

## API Reference

### POST /api/query

Process a customer service query.

**Request**
```json
{
  "query": "What documents are needed for export to Indonesia?"
}
```

**Response**
```json
{
  "answer": "For exports to Indonesia, you typically need:\n\n1. **Commercial Invoice**...",
  "citations": [
    {
      "title": "Singapore Export Procedures",
      "section": "Required Documents",
      "matched": true,
      "sourceUrls": ["https://www.customs.gov.sg/..."]
    }
  ],
  "sourcesMarkdown": "\n---\n**Sources:**\n1. [Singapore Export Procedures](https://...)",
  "confidence": {
    "level": "High",
    "reason": "5 relevant sources"
  },
  "metadata": {
    "query": "What documents are needed for export to Indonesia?",
    "chunksRetrieved": 5,
    "chunksUsed": 2,
    "model": "llama-3.1-8b-instant",
    "usage": {
      "promptTokens": 850,
      "completionTokens": 200,
      "totalTokens": 1050
    },
    "latency": {
      "retrievalMs": 150,
      "generationMs": 1200,
      "citationMs": 5,
      "totalMs": 1355
    }
  }
}
```

**Error Response**
```json
{
  "error": "Bad Request",
  "message": "Query parameter is required and must be a string"
}
```

### GET /api/health

Server health check.

**Response**
```json
{
  "status": "ok",
  "timestamp": "2026-02-01T12:00:00.000Z",
  "uptime": 3600,
  "version": "1.0.0"
}
```

---

## Development

### Project Structure

```
03_rag_pipeline/
├── src/
│   ├── index.js              # Express server entry
│   ├── config.js             # Configuration loader
│   ├── services/
│   │   ├── retrieval.js      # ChromaDB integration
│   │   ├── llm.js            # Groq LLM service
│   │   ├── citations.js      # Citation extraction
│   │   └── pipeline.js       # RAG orchestrator
│   ├── routes/
│   │   ├── query.js          # POST /api/query
│   │   └── health.js         # GET /api/health
│   ├── prompts/
│   │   └── system.txt        # System prompt template
│   ├── middleware/
│   │   └── errorHandler.js   # Error handling
│   └── utils/
│       └── logger.js         # Logging utility
├── client/                   # React frontend (Vite)
├── scripts/                  # Python scripts
├── tests/                    # Jest unit tests
├── docs/                     # Documentation
├── reports/                  # Generated reports
└── chroma_data/              # Vector database (gitignored)
```

### Adding Documents to Knowledge Base

1. Add markdown file to `../01_knowledge_base/kb/`
2. Include YAML frontmatter with metadata
3. Run ingestion pipeline:
   ```bash
   cd ../02_ingestion_pipeline
   python scripts/ingest.py
   ```
4. Verify with retrieval test

### Code Style

- ES Modules (`import`/`export`)
- JSDoc comments for public functions
- Async/await for asynchronous code
- Error handling with try/catch

---

## Testing

### Unit Tests (Jest)

```bash
# Run all tests
npm test

# Run specific test file
npm test -- --testPathPattern=citations

# Run with coverage
npm test -- --coverage
```

**Current Status**: 105 tests passing across 6 test suites

### E2E Tests (Python)

```bash
# Ensure backend is running
npm start

# Run E2E test suite
python scripts/e2e_test_suite.py

# View report
cat reports/e2e_test_report.md
```

**Test Categories**:
| Category | Tests | Description |
|----------|-------|-------------|
| Happy Path | 10 | Factual queries |
| Multi-Source | 5 | Multi-document queries |
| Out-of-Scope | 5 | Decline detection |
| Edge Cases | 5 | Unicode, injection, long queries |
| Concurrent | 3 | Parallel requests |
| Error Recovery | 2 | Timeout, malformed requests |

**Current Status**: 30/30 tests passing (100%)

---

## Performance

| Metric | Value |
|--------|-------|
| Average Latency | ~2-4 seconds |
| P95 Latency | ~10-12 seconds |
| Max Latency | ~15 seconds |
| Concurrent Capacity | 3+ simultaneous |

---

## Known Limitations

1. **LLM Variability**: Response times vary based on Groq API load (1-15s)
2. **Knowledge Scope**: Limited to 29 documents in knowledge base
3. **No Real-Time Data**: Cannot provide live tracking, rates, or bookings
4. **Citation Matching**: Some responses may show fewer citations than expected

For detailed information, see [docs/03_known_issues.md](docs/03_known_issues.md).

---

## Troubleshooting

### Common Issues

**ChromaDB Connection Error**
```bash
# Ensure Python bridge is working
cd ../02_ingestion_pipeline
python scripts/verify_ingestion.py
```

**Groq API Timeout**
- Check API key is valid
- Verify network connectivity
- Retry with shorter query

**No Chunks Retrieved**
- Rephrase query with different keywords
- Check knowledge base has relevant content

---

## License

Internal use only - Waypoint Logistics Pte Ltd

---

*Documentation generated: 2026-02-01*
