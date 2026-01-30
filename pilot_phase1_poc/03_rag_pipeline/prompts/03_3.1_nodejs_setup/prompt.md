# Task 3.1: Create Node.js Project Structure

## Persona

> You are a Node.js developer with expertise in Express.js APIs and project scaffolding.
> You follow clean architecture principles and create maintainable, well-organized codebases.

---

## Context

### Project Background
Waypoint is a RAG-based customer service co-pilot. The retrieval quality testing is complete (76% hit rate, PROCEED decision). Now we build the Node.js backend that will serve as the API layer for the RAG pipeline.

### Current State
- Ingestion pipeline complete at `03_rag_pipeline/ingestion/` (Python)
- ChromaDB populated with 483 chunks
- No Node.js project exists yet in `03_rag_pipeline/`

### Reference Documents
- `03_rag_pipeline/docs/00_week2_rag_pipeline_plan.md` - Architecture details
- `03_rag_pipeline/docs/01_implementation_roadmap.md` - Task specifications

### Dependencies
- Task 1.1: Copy KB and Ingestion ✅
- Task 1.2: Fix source_urls ✅
- Task 2.1: Retrieval Quality Test ✅
- Task 2.2: Decision Gate (PROCEED) ✅

---

## Task

### Objective
Create the Node.js project structure with Express.js, including all directories, configuration files, and a basic test setup.

### Requirements

1. **Create package.json**
   - Project name: `waypoint-rag-pipeline`
   - Type: ES modules (`"type": "module"`)
   - Scripts: start, dev, test
   - All required dependencies

2. **Create directory structure**
   - `src/` with subdirectories for routes, services, prompts, utils
   - `tests/` for Jest tests
   - Placeholder files with JSDoc comments

3. **Create environment configuration**
   - `.env.example` with all required variables (documented)
   - `.env` copied from example (gitignored)
   - `src/config.js` to load and export config

4. **Configure Jest for testing**
   - `jest.config.js` for ES modules
   - One passing placeholder test

5. **Create placeholder files**
   - Each file should have proper JSDoc and export structure
   - Placeholder functions that throw "Not implemented"

### Specifications

**package.json**:
```json
{
  "name": "waypoint-rag-pipeline",
  "version": "1.0.0",
  "description": "RAG pipeline API for Waypoint customer service co-pilot",
  "type": "module",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "dev": "node --watch src/index.js",
    "test": "node --experimental-vm-modules node_modules/jest/bin/jest.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "chromadb": "^1.8.1",
    "openai": "^4.28.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "supertest": "^6.3.4"
  }
}
```

**.env.example**:
```bash
# Server
PORT=3000
NODE_ENV=development

# ChromaDB
CHROMA_PATH=./ingestion/chroma_db
COLLECTION_NAME=waypoint_kb

# Retrieval
RETRIEVAL_TOP_K=10
RELEVANCE_THRESHOLD=0.15
MAX_CONTEXT_TOKENS=2000

# LLM (Groq)
LLM_PROVIDER=groq
LLM_API_KEY=your_groq_api_key_here
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500
```

**Target Directory Structure**:
```
03_rag_pipeline/
├── src/
│   ├── index.js              # Express app entry point
│   ├── config.js             # Environment config loader
│   ├── routes/
│   │   ├── index.js          # Route aggregator
│   │   └── query.js          # POST /api/query endpoint
│   ├── services/
│   │   ├── index.js          # Service exports
│   │   ├── pipeline.js       # Orchestrates RAG flow
│   │   ├── retrieval.js      # ChromaDB queries
│   │   ├── llm.js            # Groq API calls
│   │   └── embedding.js      # Query embedding (calls Python)
│   ├── prompts/
│   │   └── system.txt        # System prompt template (placeholder)
│   └── utils/
│       └── logger.js         # Structured logging
├── tests/
│   ├── setup.js              # Jest setup
│   └── placeholder.test.js   # Passing placeholder test
├── .env                      # Local config (gitignored)
├── .env.example              # Config template
├── jest.config.js            # Jest configuration
└── package.json
```

**src/index.js** (placeholder):
```javascript
/**
 * Waypoint RAG Pipeline API
 *
 * Express server that provides the /api/query endpoint
 * for the customer service co-pilot.
 */

import express from 'express';
import cors from 'cors';
import { config } from './config.js';
import { queryRouter } from './routes/index.js';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api', queryRouter);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
const PORT = config.port;
app.listen(PORT, () => {
  console.log(`Waypoint RAG Pipeline running on port ${PORT}`);
});

export default app;
```

**src/config.js**:
```javascript
/**
 * Configuration module
 * Loads environment variables and exports typed config object.
 */

import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env from project root
dotenv.config({ path: join(__dirname, '..', '.env') });

export const config = {
  // Server
  port: parseInt(process.env.PORT || '3000', 10),
  nodeEnv: process.env.NODE_ENV || 'development',

  // ChromaDB
  chromaPath: process.env.CHROMA_PATH || './ingestion/chroma_db',
  collectionName: process.env.COLLECTION_NAME || 'waypoint_kb',

  // Retrieval
  retrievalTopK: parseInt(process.env.RETRIEVAL_TOP_K || '10', 10),
  relevanceThreshold: parseFloat(process.env.RELEVANCE_THRESHOLD || '0.15'),
  maxContextTokens: parseInt(process.env.MAX_CONTEXT_TOKENS || '2000', 10),

  // LLM
  llmProvider: process.env.LLM_PROVIDER || 'groq',
  llmApiKey: process.env.LLM_API_KEY,
  llmBaseUrl: process.env.LLM_BASE_URL || 'https://api.groq.com/openai/v1',
  llmModel: process.env.LLM_MODEL || 'llama-3.1-8b-instant',
  llmTemperature: parseFloat(process.env.LLM_TEMPERATURE || '0.3'),
  llmMaxTokens: parseInt(process.env.LLM_MAX_TOKENS || '500', 10),
};
```

**tests/placeholder.test.js**:
```javascript
/**
 * Placeholder test to verify Jest is working
 */

describe('Project Setup', () => {
  test('Jest is configured correctly', () => {
    expect(true).toBe(true);
  });

  test('Environment can be loaded', async () => {
    const { config } = await import('../src/config.js');
    expect(config.port).toBeDefined();
    expect(typeof config.port).toBe('number');
  });
});
```

### Constraints
- Use ES modules (import/export), not CommonJS
- Do NOT implement actual service logic (placeholder only)
- Do NOT install dependencies (user will run `npm install`)
- Keep placeholder files minimal but with proper structure

### Acceptance Criteria
- [ ] `package.json` created with all dependencies
- [ ] Directory structure matches specification
- [ ] `.env.example` has all config variables documented
- [ ] `.env` created (copy of example)
- [ ] `src/config.js` loads all environment variables
- [ ] `jest.config.js` configured for ES modules
- [ ] `npm install` runs successfully
- [ ] `npm test` passes (placeholder test)
- [ ] `npm start` starts server on port 3000

### TDD Requirements
- [ ] `tests/placeholder.test.js` passes
- [ ] Config loading test passes

---

## Format

### Output Structure
All files created as specified in target directory structure.

### Code Style
- ES modules (import/export)
- JSDoc comments for all exported functions
- camelCase for variables/functions
- PascalCase for classes
- 2-space indentation

### Validation Commands

```bash
cd pilot_phase1_poc/03_rag_pipeline

# Install dependencies
npm install

# Run tests (should pass)
npm test

# Start server (should start on port 3000)
npm start

# In another terminal, test health endpoint
curl http://localhost:3000/api/health
# Expected: {"status":"ok","timestamp":"..."}
```

### Expected Test Output
```
PASS  tests/placeholder.test.js
  Project Setup
    ✓ Jest is configured correctly
    ✓ Environment can be loaded

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
```
