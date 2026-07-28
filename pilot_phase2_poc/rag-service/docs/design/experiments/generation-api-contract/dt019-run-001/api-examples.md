# DT019 API Examples

Status: Historical synthetic schema examples; not current corpus/model authority

> These examples preserve DT019 design history. Values such as
> `retrieval_eligible: true` for `APAC-001` and
> `model_id: llama-3.3-70b-versatile` do not override the current source
> registry or reopened model-selection decision. `RAG-DT024` and reopened
> `RAG-DT015` must supply current executable values.
Run: `dt019-run-001`

## Positive Request

```http
POST /api/v1/query
Content-Type: application/json
```

```json
{
  "query": "What public workflow does Singapore Customs describe for obtaining an import permit?",
  "market": "SG",
  "debug": false
}
```

## Positive Response

```json
{
  "schema_version": "rag.query_response.v1",
  "request_id": "req-dt019-gq001",
  "answer_type": "answer",
  "answer": "Singapore Customs describes import permit application as a TradeNet-based workflow involving UEN registration, Customs Account activation, and permit submission through TradeNet.",
  "citations": [
    {
      "approved_source": "APAC-001",
      "document_id": "APAC-001",
      "snapshot_id": "snap-20260716-apac-001",
      "chunk_id": "APAC-001-snap-20260716-apac-001-hsr-002",
      "chunk_strategy": "hybrid_structure_recursive_v1",
      "heading_path": "Singapore Customs Import Permit Candidate > Source-Derived Notes",
      "source_uri": "https://www.customs.gov.sg/doing-business/import-operations/import-procedures/obtain-a-customs-import-permit/",
      "candidate_sha256": "4ea671e4bd08e5de9f65fef1365011c7555246f6bc4c8ef357c65a0f3ed20b77",
      "reuse_mode": "cite_and_summarize",
      "license_sensitive": false,
      "retrieval_eligible": true,
      "quote_policy": "cite_and_summarize"
    }
  ],
  "safety": {
    "refusal": false,
    "safe_response": false,
    "reason_code": null,
    "safety_notes": [],
    "blocked_stage": null
  },
  "planner": {
    "relevance_classification": "in_scope",
    "intent": "regulatory_explanation",
    "retrieval_allowed": true,
    "safe_response_id": null,
    "markets": ["SG"],
    "source_filters": ["APAC-001"],
    "reasons": ["matched import permit workflow terms"]
  },
  "retrieval": {
    "retrieval_mode": "exact_match_boosted_hybrid",
    "retrieval_performed": true,
    "low_confidence": false,
    "candidate_count_before_filter": 12,
    "candidate_count_after_filter": 4,
    "context_chunk_count": 1,
    "scores_visible": true
  },
  "generation": {
    "provider_label": "groq",
    "model_id": "llama-3.3-70b-versatile",
    "latency_ms": 650.0,
    "retry_count": 0,
    "schema_valid": true,
    "fallback_used": false
  },
  "errors": []
}
```

## Unsupported Operational Request

```json
{
  "query": "What is the current order status for shipment WP-12345?"
}
```

Expected behavior:

- planner blocks retrieval;
- generation is not called unless formatting is explicitly mocked;
- response is a safe refusal with no citations.

```json
{
  "schema_version": "rag.query_response.v1",
  "request_id": "req-dt019-gq009",
  "answer_type": "refusal",
  "answer": "I cannot answer live shipment or order status from this public regulatory RAG service.",
  "citations": [],
  "safety": {
    "refusal": true,
    "safe_response": true,
    "reason_code": "unsupported_operational",
    "safety_notes": ["Live shipment state is outside the approved public regulatory source corpus."],
    "blocked_stage": "planner"
  },
  "planner": {
    "relevance_classification": "unsupported_operational",
    "intent": "unsupported_operational_status",
    "retrieval_allowed": false,
    "safe_response_id": "safe_unsupported_operational",
    "markets": [],
    "source_filters": [],
    "reasons": ["matched shipment/order status pattern"]
  },
  "retrieval": {
    "retrieval_mode": "no_retrieval_safe_response",
    "retrieval_performed": false,
    "low_confidence": false,
    "candidate_count_before_filter": 0,
    "candidate_count_after_filter": 0,
    "context_chunk_count": 0,
    "scores_visible": false
  },
  "generation": {
    "provider_label": null,
    "model_id": null,
    "latency_ms": null,
    "retry_count": 0,
    "schema_valid": true,
    "fallback_used": false
  },
  "errors": []
}
```

## License-Sensitive Request

```json
{
  "query": "Reproduce the HS Nomenclature 2022 headings from WCO."
}
```

Expected behavior:

- do not retrieve WCO answer text;
- optionally expose metadata-only exclusion boundary;
- return refusal/no-evidence with `license_sensitive`.

## Malformed Model Output Fallback

If the model returns malformed JSON twice:

```json
{
  "schema_version": "rag.query_response.v1",
  "request_id": "req-dt019-malformed",
  "answer_type": "error_fallback",
  "answer": "I could not produce a validated answer for this request. Please try again later.",
  "citations": [],
  "safety": {
    "refusal": false,
    "safe_response": true,
    "reason_code": "malformed_output",
    "safety_notes": ["The model output did not match the required schema after retry."],
    "blocked_stage": "validation"
  },
  "planner": {
    "relevance_classification": "in_scope",
    "intent": "regulatory_explanation",
    "retrieval_allowed": true,
    "safe_response_id": null,
    "markets": ["SG"],
    "source_filters": ["APAC-001"],
    "reasons": []
  },
  "retrieval": {
    "retrieval_mode": "metadata_filtered_hybrid",
    "retrieval_performed": true,
    "low_confidence": false,
    "candidate_count_before_filter": 12,
    "candidate_count_after_filter": 4,
    "context_chunk_count": 4,
    "scores_visible": true
  },
  "generation": {
    "provider_label": "groq",
    "model_id": "llama-3.3-70b-versatile",
    "latency_ms": 1200.0,
    "retry_count": 1,
    "schema_valid": false,
    "fallback_used": true
  },
  "errors": [
    {
      "code": "malformed_output",
      "message": "Model output failed schema validation after retry.",
      "stage": "validation"
    }
  ]
}
```
