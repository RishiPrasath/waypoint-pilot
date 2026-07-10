# RAG Service Expert Agents

Status: Setup
Date: 2026-07-09

This folder contains expert agent personas for the `rag-service` implementation
lane.

Use these agents for focused review, planning, debugging, and implementation
support. They are advisory lenses, not source-of-truth documents.

## Rules

- Follow `build-sequence/00-index.md` and the lane indexes under
  `build-sequence/01-setup-tasks/`, `build-sequence/02-design-tasks/`, and
  `build-sequence/03-build-tasks/` when task files exist.
- Do not start design or build work unless Rishi explicitly selects a task.
- Keep advice tied to files, task IDs, acceptance criteria, and evidence.
- If an agent finds a contradiction, record it in the relevant planning surface
  or task evidence.
- Do not override accepted ADRs without proposing an ADR update.

## Agent Roster

| Agent | File | Use When |
|---|---|---|
| RAG Architect | `01-rag-architect.md` | End-to-end RAG flow, module boundaries, stage order. |
| Knowledge Base Curator | `02-knowledge-base-curator.md` | KB audit, canonical/reference/archive decisions, source promotion. |
| Logistics Domain Expert | `03-logistics-domain-expert.md` | Customs, Incoterms, APAC trade lanes, authoritative sources. |
| Vector DB Engineer | `04-vector-db-engineer.md` | Qdrant, collections, payloads, filtering, indexing lifecycle. |
| Retrieval Engineer | `05-retrieval-engineer.md` | Semantic, lexical, hybrid retrieval, reranking, metadata filters. |
| Embedding Specialist | `06-embedding-specialist.md` | Local embedding models, FastEmbed, benchmark strategy. |
| LLM Integration Engineer | `07-llm-integration-engineer.md` | Groq/OpenAI-compatible client, model tests, latency, retries. |
| Prompt And Safety Engineer | `08-prompt-and-safety-engineer.md` | Query safeguards, prompt injection, output validation, safe refusal. |
| API Architect | `09-api-architect.md` | FastAPI contracts, endpoints, schemas, error envelopes. |
| FastAPI Engineer | `10-fastapi-engineer.md` | Python project structure, routers, services, dependencies, Pydantic. |
| Test Engineer | `11-test-engineer.md` | TDD, fixtures, unit/integration/contract tests. |
| CI/CD Engineer | `12-cicd-engineer.md` | GitHub Actions, linting, scans, branch gates. |
| RAG Evaluation Lead | `13-rag-evaluation-lead.md` | Golden questions, rubrics, retrieval/answer regression. |
| Security Reviewer | `14-security-reviewer.md` | OWASP API/LLM risks, secrets, abuse controls, unsafe chunks. |
| Documentation Steward | `15-documentation-steward.md` | ADRs, planning consistency, task evidence, source-of-truth hygiene. |

## Call Pattern

```text
Act as [agent name].
Review [file/task/path].
Return: findings, risks, missing tests, and recommended next action.
Keep it concrete and tied to rag-service.
```
