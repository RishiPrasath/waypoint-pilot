# Evaluation Report

**Date**: 2026-02-10 10:28
**Run ID**: eval-2026-02-10T10-28-40
**Queries**: 50 (38 in-scope, 12 OOS)
**Successful**: 50 / 50

---

## Aggregate Metrics

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Deflection Rate | 89.5% | >= 40.0% | PASS |
| Citation Accuracy | 60.5% | >= 80.0% | FAIL |
| Hallucination Rate | 0.0% | < 15.0% | PASS |
| OOS Handling | 100.0% | >= 90.0% | PASS |
| Avg Latency | 1314.0ms | < 5000.0ms | PASS |
| Latency < 5s | 100.0% | - | - |

---

## Per-Category Breakdown

| Category | Queries | Deflection | Citation | Hallucination | Avg Latency |
|----------|---------|------------|----------|--------------|-------------|
| booking | 10 | 80.0% | 70.0% | 0.0% | 1474ms |
| customs | 10 | 90.0% | 90.0% | 0.0% | 1498ms |
| carrier | 10 | 85.7% | 14.3% | 0.0% | 1263ms |
| sla | 10 | 100.0% | 50.0% | 0.0% | 1223ms |
| edge_case | 10 | 100.0% | 100.0% | 0.0% | 1111ms |

---

## must_contain Failures

| Query | Missing Keywords |
|-------|-----------------|
| Q-04 | shipping instructions, Maersk |
| Q-08 | free on board |
| Q-12 | classification |
| Q-27 | ONE, Surabaya |

## Citation Missing (In-Scope)

| Query | Confidence |
|-------|-----------|
| Q-03 | Low |
| Q-04 | Low |
| Q-10 | Low |
| Q-17 | Low |
| Q-23 | Low |
| Q-25 | Low |
| Q-27 | Low |
| Q-28 | Low |
| Q-29 | Low |
| Q-30 | Low |
| Q-34 | Low |
| Q-35 | Low |
| Q-36 | Low |
| Q-38 | Low |
| Q-40 | Low |

---

## Raw Query Results

| ID | Category | Confidence | Deflect | Citation | Halluc | OOS | Latency | Pass |
|----|----------|------------|---------|----------|--------|-----|---------|------|
| Q-01 | booking | Low | PASS | PASS | PASS | - | 1946ms | PASS |
| Q-02 | booking | Low | PASS | PASS | PASS | - | 1277ms | PASS |
| Q-03 | booking | Low | PASS | FAIL | PASS | - | 1930ms | FAIL |
| Q-04 | booking | Low | FAIL | FAIL | PASS | - | 993ms | FAIL |
| Q-05 | booking | Medium | PASS | PASS | PASS | - | 1464ms | PASS |
| Q-06 | booking | Medium | PASS | PASS | PASS | - | 1344ms | PASS |
| Q-07 | booking | Medium | PASS | PASS | PASS | - | 1618ms | PASS |
| Q-08 | booking | Low | FAIL | PASS | PASS | - | 1503ms | FAIL |
| Q-09 | booking | Low | PASS | PASS | PASS | - | 1728ms | PASS |
| Q-10 | booking | Low | PASS | FAIL | PASS | - | 942ms | FAIL |
| Q-11 | customs | Medium | PASS | PASS | PASS | - | 1336ms | PASS |
| Q-12 | customs | Low | FAIL | PASS | PASS | - | 1738ms | FAIL |
| Q-13 | customs | Low | PASS | PASS | PASS | - | 1476ms | PASS |
| Q-14 | customs | Low | PASS | PASS | PASS | - | 1860ms | PASS |
| Q-15 | customs | Low | PASS | PASS | PASS | - | 1284ms | PASS |
| Q-16 | customs | Low | PASS | PASS | PASS | - | 1472ms | PASS |
| Q-17 | customs | Low | PASS | FAIL | PASS | - | 1113ms | FAIL |
| Q-18 | customs | Low | PASS | PASS | PASS | - | 1477ms | PASS |
| Q-19 | customs | Medium | PASS | PASS | PASS | - | 1698ms | PASS |
| Q-20 | customs | Medium | PASS | PASS | PASS | - | 1529ms | PASS |
| Q-21 | carrier | Low | PASS | FAIL | PASS | PASS | 1017ms | FAIL |
| Q-22 | carrier | Low | PASS | FAIL | PASS | PASS | 1312ms | FAIL |
| Q-23 | carrier | Low | PASS | FAIL | PASS | - | 1369ms | FAIL |
| Q-24 | carrier | Low | PASS | PASS | PASS | - | 1848ms | PASS |
| Q-25 | carrier | Low | PASS | FAIL | PASS | - | 1041ms | FAIL |
| Q-26 | carrier | Low | PASS | FAIL | PASS | PASS | 988ms | FAIL |
| Q-27 | carrier | Low | FAIL | FAIL | PASS | - | 1048ms | FAIL |
| Q-28 | carrier | Low | PASS | FAIL | PASS | - | 1047ms | FAIL |
| Q-29 | carrier | Low | PASS | FAIL | PASS | - | 1908ms | FAIL |
| Q-30 | carrier | Low | PASS | FAIL | PASS | - | 1049ms | FAIL |
| Q-31 | sla | Medium | PASS | PASS | PASS | - | 1401ms | PASS |
| Q-32 | sla | Medium | PASS | PASS | PASS | - | 1253ms | PASS |
| Q-33 | sla | Low | PASS | PASS | PASS | - | 1492ms | PASS |
| Q-34 | sla | Low | PASS | FAIL | PASS | - | 957ms | FAIL |
| Q-35 | sla | Low | PASS | FAIL | PASS | - | 975ms | FAIL |
| Q-36 | sla | Low | PASS | FAIL | PASS | - | 950ms | FAIL |
| Q-37 | sla | Low | PASS | PASS | PASS | - | 1649ms | PASS |
| Q-38 | sla | Low | PASS | FAIL | PASS | - | 994ms | FAIL |
| Q-39 | sla | Low | PASS | PASS | PASS | - | 1590ms | PASS |
| Q-40 | sla | Low | PASS | FAIL | PASS | - | 968ms | FAIL |
| Q-41 | edge_case | Low | PASS | FAIL | PASS | PASS | 1320ms | FAIL |
| Q-42 | edge_case | Low | PASS | FAIL | PASS | PASS | 973ms | FAIL |
| Q-43 | edge_case | Low | PASS | FAIL | PASS | PASS | 963ms | FAIL |
| Q-44 | edge_case | Low | PASS | PASS | PASS | - | 1781ms | PASS |
| Q-45 | edge_case | Low | PASS | FAIL | PASS | PASS | 1121ms | FAIL |
| Q-46 | edge_case | Low | PASS | FAIL | PASS | PASS | 981ms | FAIL |
| Q-47 | edge_case | Low | PASS | FAIL | PASS | PASS | 986ms | FAIL |
| Q-48 | edge_case | Low | PASS | FAIL | PASS | PASS | 1012ms | FAIL |
| Q-49 | edge_case | Low | PASS | FAIL | PASS | PASS | 990ms | FAIL |
| Q-50 | edge_case | Low | PASS | FAIL | PASS | PASS | 979ms | FAIL |
