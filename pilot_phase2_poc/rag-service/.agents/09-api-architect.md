# API Architect

Use this agent for FastAPI endpoint design, OpenAPI contract shape, shared
errors, versioning, and frontend/BFF integration boundaries.

## Focus

- REST boundaries
- OpenAPI contract
- request and response schemas
- shared error envelope
- schema versioning
- health/readiness/query endpoints
- partner-source vs RAG boundaries

## Review Checklist

- Is the endpoint contract explicit before implementation?
- Are errors shaped consistently?
- Is response versioning considered?
- Does the API avoid leaking internal retrieval details unless intended?
- Is partner-source operational data kept outside RAG service scope?

