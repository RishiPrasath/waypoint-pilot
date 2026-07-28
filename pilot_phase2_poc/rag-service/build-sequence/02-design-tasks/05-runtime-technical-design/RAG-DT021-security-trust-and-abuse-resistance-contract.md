# RAG-DT021: Security, Trust, And Abuse-Resistance Contract

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-DT021` |
| Lane | design |
| Dependencies | `RAG-DT008`, `RAG-DT012`, `RAG-DT014`, `RAG-DT017` |
| Blocks | `RAG-DT013`, `RAG-BT012`, `RAG-BT015`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT019`, `RAG-BT022` |
| Responsible | Security/RAG engineer |
| Accountable approver | AI/security owner |
| Required reviewers | Platform owner, corpus/data owner, service owner |
| Branch | `codex/rag-dt021-security-trust-abuse-contract` |
| Worktree | `C:\tmp\rag-dt021-security-trust-abuse-contract` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT021-security-trust-abuse-contract.md` |

## 1. Objective And Scope

Define the service trust boundaries and the controls needed to prevent unsafe
source ingestion, indirect prompt injection, provider/API abuse, data leakage,
and uncontrolled resource consumption.

This task must distinguish:

- a local, fixture-only proof of concept;
- a shared internal service;
- an externally reachable production service.

It must not silently apply production language to a local-only design.

## 2. Dependencies And Gates

Use the accepted source registry, snapshot, Qdrant, and generation/API
contracts as inputs. Reopen `RAG-DT019` and update it wherever this task changes
the prompt, response, citation, API, or provider contract.

Before this task makes any live provider call, record the G0 containment state:
the historical model decision is prohibited as a current default and the
exposed credential is either rotated or explicitly recorded as still pending.
The record contains no secret material. A pending rotation permits fixture-only
design work but prohibits live provider evaluation or runtime traffic.

No runtime task may treat deterministic query-planner phrase matching as a
security boundary.

## 3. Expected Artifacts

```text
docs/design/security-trust-and-abuse-resistance-contract.md
docs/design/threat-model.md
docs/evaluation/adversarial-rag-cases.yaml
build-evidence/RAG-DT021-security-trust-abuse-contract.md
```

## 4. Acceptance Criteria

- Data-flow and trust-boundary diagrams cover caller, FastAPI, source
  acquisition, registry, chunking, Qdrant, Groq-compatible provider, logs, and
  CI.
- The deployment tier selects or explicitly defers authentication,
  authorization, tenant isolation, CORS/trusted-host rules, TLS, and secret
  management.
- Request byte/token limits, concurrency limits, timeouts, rate/cost controls,
  provider quota behavior, and their numeric budgets are specified by tier.
- Outbound provider access has an allowlist, redirect policy, TLS validation,
  timeout, and response-size policy.
- Source acquisition defines provenance, upstream hashes, diff review,
  quarantine, promotion, revocation, and poisoning response.
- Curator annotations and review notes cannot enter the answerable corpus.
- A named owner and accountable approver are assigned before a control is
  deferred; no control may be deferred anonymously.
- Direct and indirect prompt injection, obfuscation, multilingual/split
  payloads, malicious retrieved chunks, and poisoned-source cases are tested.
- Logging, retention, redaction, privacy classification, and incident evidence
  rules are explicit.
- Each control is mapped to a build task, verification command, owner, and
  allowed deployment tier.

## 5. Preflight

Create the standard task branch and worktree from refreshed `origin/main`.
Confirm the current design and task indexes still identify `RAG-DT013` as the
final design-to-build gate.

## 6. Red Check

```powershell
Test-Path docs/design/security-trust-and-abuse-resistance-contract.md
Test-Path docs/evaluation/adversarial-rag-cases.yaml
```

Both results must be `False` before implementation.

## 7. Implementation Or Design Work

1. Draw data flows and enumerate assets, actors, entry points, and trust
   boundaries.
2. Classify the deployment tiers and make every deferred control tier-specific.
3. Threat-model source poisoning, indirect prompt injection, API abuse,
   provider failure, data disclosure, denial of wallet/service, and log leaks.
4. Define preventive, detective, and recovery controls.
5. Add executable adversarial fixtures and required outcomes.
6. Update `RAG-DT019` and all affected build tasks.
7. Record G0 containment evidence without exposing a key, token, or provider
   response body.

## 8. Verification Matrix

| Check | Required Result |
|---|---|
| Threat model coverage | Every trust boundary has threats and controls |
| Adversarial cases | Direct, indirect, poisoned, obfuscated, and multilingual cases exist |
| API controls | Auth decision, limits, timeouts, quotas, and outbound policy are explicit |
| Corpus controls | Provenance, quarantine, promotion, revocation, and annotation exclusion are explicit |
| Containment | G0 state and live-call prohibition are explicit and non-secret |
| Build impact | Every control has an owner, task, and verification method |

## 9. PR Handoff

Summarize the selected deployment tier, top threats, mandatory controls,
accepted deferrals, affected tasks, and verification evidence.

## 10. Merge And Closeout

Merge only after security, RAG/data, API, and operations reviewers agree that
the chosen deployment tier is internally consistent. Keep `RAG-DT013` blocked
until the affected task files are reconciled.

## 11. Out Of Scope And Deferred Work

Runtime implementation is out of scope. A control may be deferred only with a
named owner, permitted deployment tier, expiry/review date, and explicit
failure mode.
