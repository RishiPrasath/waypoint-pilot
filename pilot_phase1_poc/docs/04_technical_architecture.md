# 04 - Technical Architecture

**Document Type**: Technical Specification  
**Pilot**: Waypoint Phase 1 POC  
**Version**: 1.0

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│                   (Simple Web UI or CLI)                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Node.js Backend                            │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │   Query     │  │   RAG        │  │   Response            │  │
│  │   Handler   │→ │   Pipeline   │→ │   Generator           │  │
│  └─────────────┘  └──────────────┘  └───────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │   ChromaDB   │ │  Embedding   │ │    LLM       │
        │   (Vector)   │ │    Model     │ │    API       │
        └──────────────┘ └──────────────┘ └──────────────┘
```

---

## Component Selection

### Design Principles
1. **Free or very low cost** — POC budget < $10 total
2. **Local-first** — Development works offline where possible
3. **Simple** — Solo dev maintainability
4. **Extensible** — Can scale to Pinecone/production later

---

## Core Components

### 1. Vector Database: ChromaDB

**Why ChromaDB**:
- Free and open source
- Runs locally (no cloud dependency)
- Simple Python/JS API
- Good enough for 25-30 documents
- Easy migration path to Pinecone later

**Installation**:
```bash
# Python (recommended for document processing)
pip install chromadb

# Or via Docker
docker pull chromadb/chroma
docker run -p 8000:8000 chromadb/chroma
```

**Alternative Considered**: Pinecone
- Better for production but has usage limits on free tier
- Save for Phase 2 deployment

---

### 2. Embedding Model: Sentence Transformers (Local)

**Primary Choice**: `all-MiniLM-L6-v2`

**Why**:
- Free (runs locally)
- Fast inference
- 384-dimensional vectors (efficient storage)
- Good general-purpose performance

**Installation**:
```bash
pip install sentence-transformers
```

**Usage**:
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["Your text here"])
```

**Alternative for Higher Quality**: `all-mpnet-base-v2`
- 768 dimensions, better accuracy
- Slower, more memory
- Use if quality insufficient with MiniLM

**Cloud Alternative** (if local too slow):
- Voyage AI: 50M free tokens/month
- Cohere: Free tier available

---

### 3. LLM: Groq API (Llama 3)

**Primary Choice**: Groq API with Llama 3.1 8B

**Why Groq**:
- Free tier: Generous for POC
- Fast inference (tokens/second)
- Good quality with Llama 3.1 8B
- Simple API

**Pricing** (if exceeds free tier):
- Llama 3.1 8B: ~$0.05/1M input, ~$0.08/1M output
- POC estimate: < $1 total

**Setup**:
```bash
# Get API key from console.groq.com
export GROQ_API_KEY=your_key_here
```

**Usage**:
```javascript
import Groq from 'groq-sdk';

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

const response = await groq.chat.completions.create({
  messages: [
    { role: "system", content: systemPrompt },
    { role: "user", content: userQuery }
  ],
  model: "llama-3.1-8b-instant",
  temperature: 0.3,
  max_tokens: 1024
});
```

**Alternatives**:
| Provider | Model | Free Tier | Cost |
|----------|-------|-----------|------|
| **Groq** | Llama 3.1 8B | Yes | ~$0.05-0.08/1M |
| Claude Haiku | claude-3-haiku | No | $0.25-1.25/1M |
| OpenAI | gpt-4o-mini | $5 credit | $0.15-0.60/1M |
| Together AI | Various | $5 credit | Varies |
| Ollama | Local Llama | Free | Free (local) |

**Fallback Option**: Ollama (fully local)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Run
ollama run llama3.1:8b
```
- Pro: Completely free, works offline
- Con: Requires decent hardware (16GB+ RAM recommended)

---

### 4. Backend: Node.js

**Framework**: Express.js (minimal)

**Why Node.js**:
- Already in your tech stack
- Simple REST API setup
- Good LLM SDK support
- Easy integration with frontend

**Project Structure**:
```
waypoint-poc/
├── src/
│   ├── index.js           # Express server
│   ├── routes/
│   │   └── query.js       # Query endpoint
│   ├── services/
│   │   ├── embedding.js   # Embedding service
│   │   ├── retrieval.js   # ChromaDB retrieval
│   │   └── llm.js         # LLM generation
│   └── utils/
│       └── prompts.js     # System prompts
├── scripts/
│   ├── ingest.py          # Document ingestion
│   └── process_docs.py    # Document processing
├── knowledge_base/
│   └── [documents]
├── tests/
│   └── test_queries.js
├── package.json
└── .env
```

**Key Dependencies**:
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "groq-sdk": "^0.3.0",
    "chromadb": "^1.7.0",
    "dotenv": "^16.3.1",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
```

---

### 5. Document Processing: Python Scripts

**Why Python for Ingestion**:
- Better document processing libraries
- sentence-transformers native Python
- ChromaDB works well with Python
- One-time ingestion, doesn't need to be in Node

**Dependencies**:
```txt
# requirements.txt
chromadb==0.4.22
sentence-transformers==2.2.2
langchain==0.1.0
langchain-text-splitters==0.0.1
pypdf==3.17.4
markdown==3.5.1
python-frontmatter==1.1.0
```

**Ingestion Pipeline**:
```python
# scripts/ingest.py
import chromadb
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Load documents
# 2. Extract metadata
# 3. Chunk documents
# 4. Generate embeddings
# 5. Store in ChromaDB
```

---

### 6. User Interface: Simple Web UI

**Option A: Minimal HTML/JS** (Recommended for POC)

```html
<!-- Single page, no framework -->
<!DOCTYPE html>
<html>
<head>
    <title>Waypoint Co-Pilot</title>
    <style>
        /* Simple CSS */
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="messages"></div>
        <input type="text" id="query-input" placeholder="Ask a question...">
        <button onclick="sendQuery()">Send</button>
    </div>
    <script>
        async function sendQuery() {
            const query = document.getElementById('query-input').value;
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const data = await response.json();
            displayResponse(data);
        }
    </script>
</body>
</html>
```

**Option B: CLI Interface** (Even simpler)

```javascript
// cli.js
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function askQuestion() {
    rl.question('You: ', async (query) => {
        const response = await queryPipeline(query);
        console.log(`\nAssistant: ${response.answer}\n`);
        console.log(`Sources: ${response.sources.join(', ')}\n`);
        askQuestion();
    });
}

askQuestion();
```

---

## RAG Pipeline Design

### Query Flow

```
User Query
    │
    ▼
┌─────────────────────────────────────┐
│  1. Query Processing                │
│  - Clean/normalize query            │
│  - Generate query embedding         │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  2. Retrieval                       │
│  - Search ChromaDB (top-k=5)        │
│  - Filter by relevance threshold    │
│  - Return chunks + metadata         │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  3. Context Assembly                │
│  - Format retrieved chunks          │
│  - Include source attribution       │
│  - Build prompt                     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  4. Generation                      │
│  - Send to LLM with system prompt   │
│  - Parse response                   │
│  - Extract citations                │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  5. Response Formatting             │
│  - Structure answer                 │
│  - Include sources                  │
│  - Add confidence indicator         │
└─────────────────────────────────────┘
    │
    ▼
Response to User
```

---

### System Prompt Template

```javascript
const SYSTEM_PROMPT = `You are a customer service co-pilot for a freight forwarding company in Singapore. Your role is to help CS agents find accurate information to answer customer queries.

INSTRUCTIONS:
1. Answer ONLY based on the provided context documents
2. If the information is not in the context, say "I don't have information about that in my knowledge base"
3. Always cite your sources using the format: [Source: Document Name, Section]
4. Keep answers concise but complete
5. If a query is outside freight forwarding scope, politely redirect
6. For rate or booking requests, direct to the appropriate team

CONTEXT DOCUMENTS:
{context}

USER QUERY: {query}

Provide a helpful, accurate response based on the above context.`;
```

---

### Retrieval Configuration

```javascript
// services/retrieval.js
const RETRIEVAL_CONFIG = {
    topK: 5,                    // Number of chunks to retrieve
    relevanceThreshold: 0.7,    // Minimum similarity score
    maxContextTokens: 2000,     // Token budget for context
    includeMetadata: true       // Return source info
};

async function retrieve(queryEmbedding) {
    const results = await collection.query({
        queryEmbeddings: [queryEmbedding],
        nResults: RETRIEVAL_CONFIG.topK,
        include: ['documents', 'metadatas', 'distances']
    });
    
    // Filter by relevance
    return results.filter(r => r.distance < (1 - RETRIEVAL_CONFIG.relevanceThreshold));
}
```

---

## Development Environment Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- Git

### Setup Steps

```bash
# 1. Create project
mkdir waypoint-poc && cd waypoint-poc

# 2. Initialize Node.js
npm init -y
npm install express groq-sdk chromadb dotenv cors

# 3. Create Python virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 4. Set up environment variables
echo "GROQ_API_KEY=your_key_here" > .env

# 5. Create directory structure
mkdir -p src/{routes,services,utils} scripts knowledge_base tests

# 6. Initialize ChromaDB
python -c "import chromadb; client = chromadb.PersistentClient(path='./chroma_db')"
```

---

## API Specification

### POST /api/query

**Request**:
```json
{
    "query": "What documents are needed for export to Indonesia?",
    "options": {
        "maxResults": 5,
        "includeContext": false
    }
}
```

**Response**:
```json
{
    "answer": "For sea freight export from Singapore to Indonesia, you typically need:\n\n1. Commercial Invoice...",
    "sources": [
        {
            "document": "Singapore Customs Export Guide",
            "section": "Documentation Requirements",
            "relevance": 0.89
        },
        {
            "document": "Indonesia INSW Import Requirements",
            "section": "Required Documents",
            "relevance": 0.85
        }
    ],
    "confidence": "high",
    "metadata": {
        "processingTime": 1.2,
        "tokensUsed": 450
    }
}
```

### GET /api/health

**Response**:
```json
{
    "status": "healthy",
    "components": {
        "database": "connected",
        "llm": "available",
        "documentsIndexed": 25
    }
}
```

---

## Cost Estimation

| Component | Usage Estimate | Cost |
|-----------|---------------|------|
| ChromaDB | Local | $0 |
| Sentence Transformers | Local | $0 |
| Groq API | ~50 test queries | $0 (free tier) |
| Development tools | VSCode, etc. | $0 |
| **Total** | | **$0** |

**If free tier exceeded**:
- Groq: ~$0.10 for 100 queries
- Claude Haiku fallback: ~$0.50 for 100 queries
- Maximum expected: **< $5**

---

## Migration Path to Production

### Phase 2 Upgrades

| Component | POC | Production |
|-----------|-----|------------|
| Vector DB | ChromaDB (local) | Pinecone (cloud) |
| Embedding | sentence-transformers | Voyage AI or OpenAI |
| LLM | Groq (Llama 3.1) | Metalama or Claude |
| Backend | Express | Same + Docker |
| UI | Simple HTML | React or Next.js |
| Auth | None | OAuth/SSO |

### Code Changes Required
- Swap ChromaDB client for Pinecone client
- Update embedding service for cloud API
- Add authentication middleware
- Containerize with Docker
- Add monitoring/logging

---

## Testing Strategy

### Unit Tests
```javascript
// tests/retrieval.test.js
describe('Retrieval Service', () => {
    test('returns relevant chunks for booking query', async () => {
        const query = "What documents needed for export?";
        const results = await retrieve(query);
        expect(results.length).toBeGreaterThan(0);
        expect(results[0].relevance).toBeGreaterThan(0.7);
    });
});
```

### Integration Tests
```javascript
// tests/pipeline.test.js
describe('RAG Pipeline', () => {
    test('generates sourced response', async () => {
        const response = await queryPipeline("What is FOB?");
        expect(response.answer).toContain("Free On Board");
        expect(response.sources.length).toBeGreaterThan(0);
    });
});
```

### Evaluation Tests
- Run 50 test queries from use case catalog
- Manually evaluate accuracy
- Calculate deflection rate

---

*Next Document*: [05 - Execution Roadmap](./05_execution_roadmap.md)
