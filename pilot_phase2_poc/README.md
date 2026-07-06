# Waypoint Phase 2 POC

Phase 2 turns Waypoint from a knowledge-only RAG pilot into a contract-driven logistics support platform with a chatbot frontend for customer service agents and a delivery app frontend for delivery drivers.

The current implementation focus is `partner-source`: a synthetic logistics partner API that gives Waypoint operational data for questions such as "Where is my order?", "Who is delivering it?", and "What happened to my shipment?"

## Architecture Direction

```text
chatbot frontend              delivery app frontend
for customer service agents   for delivery drivers
          \                              /
           \                            /
            -> bff orchestration layer
                 -> partner-source
                 -> rag-db
```

| Module | Role |
|--------|------|
| `partner-source` | Operational logistics truth: orders, drivers, assignments, timelines, and status events. |
| `rag-db` | Knowledge retrieval: ingestion, retrieval, query planning, citations, safeguards, and evaluation. |
| `bff` | Orchestration layer that calls backend modules through contracts and shapes client responses. |
| `chatbot-frontend` | Customer service agent chatbot experience for order questions, policy/procedure answers, citations, and escalation states. |
| `delivery-app-frontend` | Delivery driver app experience for profile, assigned orders, delivery details, and status updates. |

## Component Status

| Component | Path | Status |
|-----------|------|--------|
| Partner Source contract | `partner-source/docs/contracts/` | Slice 1 complete. |
| Partner Source Spring Boot API | `partner-source/partner-source-springboot/` | Complete and tested. |
| Partner Source FastAPI API | `partner-source/partner-source-fastapi/` | Complete and tested. |
| Partner Source parity harness | `partner-source/parity/` | Complete; latest report: 24 passed, 0 failed, 0 skipped. |
| `rag-db` | Not yet created in this repo. | Planned next component. |
| `bff` | Not yet created in this repo. | Planned after component contracts are pinned. |
| Chatbot frontend for customer service agents | Not yet created in this repo. | Planned after BFF contract. |
| Delivery app frontend for delivery drivers | Not yet created in this repo. | Planned after BFF contract. |

## Read First

```text
partner-source\README.md
partner-source\AGREED_SPEC.md
partner-source\CONTRACT_SYNC.md
partner-source\docs\00-index.md
partner-source\parity\reports\latest\parity-report.md
```

## Verification

Run module tests from the implementation folders:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test

cd ..\partner-source-fastapi
uv run pytest

cd ..\parity
python -m pytest
```

To generate the live parity report, start both services and run:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m parity_runner
```

## Next Architecture Step

The next architecture step is to pin the `rag-db` and BFF contracts. After that, the BFF should call `partner-source` for operational truth and `rag-db` for retrieved knowledge, then return shaped responses for the customer-service chatbot frontend and delivery-driver app frontend.
