# Evaluation Report

**Date**: 2026-02-10 13:43
**Run ID**: eval-2026-02-10T13-43-08
**Queries**: 50 (39 in-scope, 11 OOS)
**Successful**: 50 / 50

---

## Aggregate Metrics

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| Deflection Rate | 87.2% | >= 40.0% | PASS |
| Citation Accuracy | 96.0% | >= 80.0% | PASS |
| Citation (raw) | 97.4% | - | (includes 14 N/A queries) |
| Hallucination Rate | 2.0% | < 15.0% | PASS |
| OOS Handling | 100.0% | >= 90.0% | PASS |
| Avg Latency | 1182.0ms | < 5000.0ms | PASS |
| Latency < 5s | 100.0% | - | - |

---

## Per-Category Breakdown

| Category | Queries | Deflection | Citation | Hallucination | Avg Latency |
|----------|---------|------------|----------|--------------|-------------|
| booking | 10 | 80.0% | 100.0% | 0.0% | 1406ms |
| customs | 10 | 100.0% | 88.9% | 0.0% | 1406ms |
| carrier | 10 | 87.5% | 100.0% | 0.0% | 1058ms |
| sla | 10 | 80.0% | 100.0% | 10.0% | 1011ms |
| edge_case | 10 | 100.0% | 100.0% | 0.0% | 1027ms |

---

## must_contain Failures

| Query | Missing Keywords |
|-------|-----------------|
| Q-04 | shipping instructions, Maersk |
| Q-08 | free on board |
| Q-27 | ONE, Surabaya |
| Q-33 | coverage |
| Q-39 | liability, standard |

## Hallucination Detections

| Query | Found Signals |
|-------|--------------|
| Q-39 | I don't have |

## Citation N/A (0 chunks — correct decline)

| Query | Confidence | Reason |
|-------|-----------|--------|
| Q-04 | Low | No chunks retrieved — citation N/A |
| Q-10 | Low | No chunks retrieved — citation N/A |
| Q-17 | Low | No chunks retrieved — citation N/A |
| Q-21 | Low | No chunks retrieved — citation N/A |
| Q-22 | Low | No chunks retrieved — citation N/A |
| Q-25 | Low | No chunks retrieved — citation N/A |
| Q-27 | Low | No chunks retrieved — citation N/A |
| Q-30 | Low | No chunks retrieved — citation N/A |
| Q-34 | Low | No chunks retrieved — citation N/A |
| Q-35 | Low | No chunks retrieved — citation N/A |
| Q-36 | Low | No chunks retrieved — citation N/A |
| Q-38 | Low | No chunks retrieved — citation N/A |
| Q-39 | Low | No chunks retrieved — citation N/A |
| Q-40 | Low | No chunks retrieved — citation N/A |

## Citation Missing (In-Scope, Chunks Available)

| Query | Confidence |
|-------|-----------|
| Q-19 | Medium |

---

## Raw Query Results

| ID | Category | Confidence | Deflect | Citation | Halluc | OOS | Latency | Pass |
|----|----------|------------|---------|----------|--------|-----|---------|------|
| Q-01 | booking | Low | PASS | PASS | PASS | - | 2021ms | PASS |
| Q-02 | booking | Low | PASS | PASS | PASS | - | 1255ms | PASS |
| Q-03 | booking | Low | PASS | PASS | PASS | - | 1540ms | PASS |
| Q-04 | booking | Low | FAIL | N/A | PASS | - | 899ms | FAIL |
| Q-05 | booking | Medium | PASS | PASS | PASS | - | 1490ms | PASS |
| Q-06 | booking | Medium | PASS | PASS | PASS | - | 1334ms | PASS |
| Q-07 | booking | Medium | PASS | PASS | PASS | - | 1401ms | PASS |
| Q-08 | booking | Low | FAIL | PASS | PASS | - | 1522ms | FAIL |
| Q-09 | booking | Low | PASS | PASS | PASS | - | 1709ms | PASS |
| Q-10 | booking | Low | PASS | N/A | PASS | - | 887ms | FAIL |
| Q-11 | customs | Medium | PASS | PASS | PASS | - | 1340ms | PASS |
| Q-12 | customs | Low | PASS | PASS | PASS | - | 1610ms | PASS |
| Q-13 | customs | Low | PASS | PASS | PASS | - | 1461ms | PASS |
| Q-14 | customs | Low | PASS | PASS | PASS | - | 1707ms | PASS |
| Q-15 | customs | Low | PASS | PASS | PASS | - | 1113ms | PASS |
| Q-16 | customs | Low | PASS | PASS | PASS | - | 1681ms | PASS |
| Q-17 | customs | Low | PASS | N/A | PASS | - | 868ms | FAIL |
| Q-18 | customs | Low | PASS | PASS | PASS | - | 1303ms | PASS |
| Q-19 | customs | Medium | PASS | FAIL | PASS | - | 1636ms | FAIL |
| Q-20 | customs | Medium | PASS | PASS | PASS | - | 1343ms | PASS |
| Q-21 | carrier | Low | PASS | N/A | PASS | - | 883ms | PASS |
| Q-22 | carrier | Low | PASS | N/A | PASS | - | 865ms | PASS |
| Q-23 | carrier | Low | PASS | PASS | PASS | - | 1172ms | PASS |
| Q-24 | carrier | Low | PASS | PASS | PASS | - | 1505ms | PASS |
| Q-25 | carrier | Low | PASS | N/A | PASS | - | 869ms | FAIL |
| Q-26 | carrier | Low | PASS | N/A | PASS | PASS | 883ms | PASS |
| Q-27 | carrier | Low | FAIL | N/A | PASS | - | 863ms | FAIL |
| Q-28 | carrier | Low | PASS | N/A | PASS | PASS | 925ms | PASS |
| Q-29 | carrier | Low | PASS | PASS | PASS | - | 1728ms | PASS |
| Q-30 | carrier | Low | PASS | N/A | PASS | - | 884ms | FAIL |
| Q-31 | sla | Medium | PASS | PASS | PASS | - | 1214ms | PASS |
| Q-32 | sla | Medium | PASS | PASS | PASS | - | 1142ms | PASS |
| Q-33 | sla | Low | FAIL | PASS | PASS | - | 1242ms | FAIL |
| Q-34 | sla | Low | PASS | N/A | PASS | - | 856ms | FAIL |
| Q-35 | sla | Low | PASS | N/A | PASS | - | 851ms | FAIL |
| Q-36 | sla | Low | PASS | N/A | PASS | - | 865ms | FAIL |
| Q-37 | sla | Low | PASS | PASS | PASS | - | 1208ms | PASS |
| Q-38 | sla | Low | PASS | N/A | PASS | - | 927ms | FAIL |
| Q-39 | sla | Low | FAIL | N/A | FAIL | - | 868ms | FAIL |
| Q-40 | sla | Low | PASS | N/A | PASS | - | 940ms | FAIL |
| Q-41 | edge_case | Low | PASS | FAIL | PASS | PASS | 1268ms | FAIL |
| Q-42 | edge_case | Low | PASS | N/A | PASS | PASS | 846ms | PASS |
| Q-43 | edge_case | Low | PASS | N/A | PASS | PASS | 924ms | PASS |
| Q-44 | edge_case | Low | PASS | PASS | PASS | - | 1733ms | PASS |
| Q-45 | edge_case | Low | PASS | N/A | PASS | PASS | 1045ms | PASS |
| Q-46 | edge_case | Low | PASS | N/A | PASS | PASS | 998ms | PASS |
| Q-47 | edge_case | Low | PASS | N/A | PASS | PASS | 923ms | PASS |
| Q-48 | edge_case | Low | PASS | N/A | PASS | PASS | 847ms | PASS |
| Q-49 | edge_case | Low | PASS | N/A | PASS | PASS | 851ms | PASS |
| Q-50 | edge_case | Low | PASS | N/A | PASS | PASS | 837ms | PASS |
