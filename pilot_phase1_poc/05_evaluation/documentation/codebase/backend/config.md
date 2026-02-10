# Configuration Documentation

## Purpose

The `backend/config.js` module loads environment variables from a `.env` file and exports a typed configuration object used throughout the backend. It is the single source of truth for all runtime configuration values.

## File

| File | Purpose |
|------|---------|
| `config.js` | Loads `.env`, parses and exports all config values |

---

## Environment File Location

The `.env` file is loaded from the **project root** (one directory above `backend/`):

```js
dotenv.config({ path: join(__dirname, '..', '.env') });
```

Relative to the workspace: `pilot_phase1_poc/05_evaluation/.env`

---

## Configuration Properties

### Server

| Property | Env Variable | Type | Default | Description |
|----------|-------------|------|---------|-------------|
| `port` | `PORT` | `number` | `3000` | HTTP server listen port |
| `nodeEnv` | `NODE_ENV` | `string` | `"development"` | Runtime environment (`development`, `production`, `test`) |

### ChromaDB

| Property | Env Variable | Type | Default | Description |
|----------|-------------|------|---------|-------------|
| `chromaPath` | `CHROMA_PATH` | `string` | `"./chroma_db"` | Path to ChromaDB persistent storage directory |
| `collectionName` | `COLLECTION_NAME` | `string` | `"waypoint_kb"` | ChromaDB collection name for the knowledge base |

### Retrieval

| Property | Env Variable | Type | Default | Description |
|----------|-------------|------|---------|-------------|
| `retrievalTopK` | `RETRIEVAL_TOP_K` | `number` | `10` | Number of chunks to retrieve from ChromaDB per query |
| `relevanceThreshold` | `RELEVANCE_THRESHOLD` | `number` | `0.15` | Minimum relevance score for chunk filtering |
| `maxContextTokens` | `MAX_CONTEXT_TOKENS` | `number` | `2000` | Approximate token budget for LLM context window |

**Note on `maxContextTokens`:** The actual character limit for context formatting is `maxContextTokens * 4` (8000 characters by default), using the rough approximation of 4 characters per token. This multiplication is performed in `retrieval.js:formatContext()`.

### LLM

| Property | Env Variable | Type | Default | Description |
|----------|-------------|------|---------|-------------|
| `llmProvider` | `LLM_PROVIDER` | `string` | `"groq"` | LLM provider identifier (informational) |
| `llmApiKey` | `LLM_API_KEY` | `string` | `undefined` | **Required.** API key for the LLM provider |
| `llmBaseUrl` | `LLM_BASE_URL` | `string` | `"https://api.groq.com/openai/v1"` | OpenAI-compatible API base URL |
| `llmModel` | `LLM_MODEL` | `string` | `"llama-3.1-8b-instant"` | Model identifier for chat completions |
| `llmTemperature` | `LLM_TEMPERATURE` | `number` | `0.3` | Sampling temperature (0.0 = deterministic, 1.0 = creative) |
| `llmMaxTokens` | `LLM_MAX_TOKENS` | `number` | `500` | Maximum tokens in the LLM response |

---

## Type Parsing

All environment variables are strings. The config module applies explicit type parsing:

| Parser | Properties |
|--------|------------|
| `parseInt(value, 10)` | `port`, `retrievalTopK`, `maxContextTokens`, `llmMaxTokens` |
| `parseFloat(value)` | `relevanceThreshold`, `llmTemperature` |
| Raw string | All others |

---

## Required vs Optional

| Variable | Required | Consequence if Missing |
|----------|----------|----------------------|
| `LLM_API_KEY` | **Yes** | `initLLMClient()` throws `"LLM_API_KEY environment variable is required"` |
| All others | No | Defaults are applied (see table above) |

---

## Example `.env` File

```env
# Server
PORT=3000
NODE_ENV=development

# ChromaDB
CHROMA_PATH=./chroma_db
COLLECTION_NAME=waypoint_kb

# Retrieval
RETRIEVAL_TOP_K=10
RELEVANCE_THRESHOLD=0.15
MAX_CONTEXT_TOKENS=2000

# LLM
LLM_PROVIDER=groq
LLM_API_KEY=gsk_your_api_key_here
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=500
```

---

## Usage in Other Modules

The config is imported as a named export:

```js
import { config } from '../config.js';

// Access properties
const topK = config.retrievalTopK;
const model = config.llmModel;
```

### Consumers

| Module | Properties Used |
|--------|----------------|
| `index.js` | `port`, `nodeEnv` |
| `retrieval.js` | `collectionName`, `retrievalTopK`, `relevanceThreshold`, `maxContextTokens` |
| `llm.js` | `llmApiKey`, `llmBaseUrl`, `llmModel`, `llmTemperature`, `llmMaxTokens`, `llmProvider` |
| `pipeline.js` | `retrievalTopK`, `relevanceThreshold` |
| `logger.js` | `nodeEnv` (for log format selection) |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `dotenv` | Loads `.env` file into `process.env` |
| `url` / `path` | Resolves `__dirname` for ESM modules (no native `__dirname` in ES modules) |

### ESM `__dirname` Resolution

Since the backend uses ES modules (`import`/`export`), `__dirname` is not available natively. The config module computes it from `import.meta.url`:

```js
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
```

This pattern is also used in `retrieval.js` and `llm.js` for resolving file paths.
