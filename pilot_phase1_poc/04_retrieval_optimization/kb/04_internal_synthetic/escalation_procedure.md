---
title: Escalation Procedure
source: Internal
source_type: synthetic_internal
last_updated: 2025-01-21
last_validated: 2025-01-24
validation_method: internal_consistency_check
validation_notes: Escalation hierarchy logical; response times consistent with POL-002 SLA Policy
jurisdiction: SG
category: procedure
use_cases: [UC-4.1, UC-4.2, UC-4.3]
document_id: SOP-002
version: 2.0
retrieval_keywords:
  - escalation
  - escalation procedure
  - priority
  - P1
  - P2
  - P3
  - incident
  - complaint
  - resolution time
  - SLA breach
---

# Escalation Procedure

## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **SLA** | Service Level Agreement | Target response/resolution times per severity |
| **P1 / P2 / P3** | Priority Levels | Severity classification for escalation routing |
| **TAT** | Turnaround Time | Maximum time allowed for each escalation tier |
| **CS** | Customer Service | First-line team handling initial queries |
| **OPS** | Operations | Second-line team for operational issues |

## Document Control

| Attribute | Value |
|-----------|-------|
| **Document ID** | SOP-002 |
| **Version** | 2.0 |
| **Effective Date** | January 1, 2025 |
| **Review Date** | July 1, 2025 |
| **Owner** | Operations Director |
| **Classification** | Internal Operations |

---

## 1. Purpose

This procedure defines the escalation pathways for operational issues, customer complaints, and service failures to ensure timely resolution and appropriate management involvement.

---

## 2. Scope

Applies to:
- Customer complaints
- Operational issues
- Service delivery failures
- System outages
- Compliance concerns
- Safety incidents

---

## 3. Escalation Levels

### 3.1 Escalation Hierarchy

```
Level 4: Managing Director / CEO
    ↑
Level 3: Director / VP
    ↑
Level 2: Manager / Department Head
    ↑
Level 1: Team Lead / Supervisor
    ↑
Level 0: Front-line Staff
```

### 3.2 Level Definitions

| Level | Role | Authority |
|-------|------|-----------|
| **L0** | Customer Service Rep, Operations Exec | First response, standard resolution |
| **L1** | Team Lead, Senior Executive | Complex issues, minor exceptions |
| **L2** | Manager, Dept Head | Policy exceptions, resource allocation |
| **L3** | Director, VP | Strategic decisions, major exceptions |
| **L4** | MD, CEO | Critical/legal issues, PR concerns |

---

## 4. Issue Classification

### 4.1 Priority Matrix

| Priority | Impact | Urgency | Examples |
|----------|--------|---------|----------|
| **P1 - Critical** | Business-critical | Immediate | Shipment stuck, safety risk, legal threat |
| **P2 - High** | Major disruption | Same day | Wrong delivery, significant delay |
| **P3 - Medium** | Moderate impact | 24-48 hours | Billing errors, documentation issues |
| **P4 - Low** | Minor inconvenience | 3-5 days | Information requests, minor complaints |

### 4.2 Automatic Escalation Triggers

| Trigger | Action |
|---------|--------|
| P1 issue reported | Immediately escalate to L2 |
| SLA at 50% | Notify L1 |
| SLA breached | Escalate to L2 |
| Customer requests escalation | Honor request, escalate |
| Regulatory/legal issue | Immediately escalate to L3 |
| Media/PR concern | Immediately escalate to L4 |

---

## 5. Escalation Process

### 5.1 Standard Escalation Flow

**Step 1: Initial Assessment (L0)**
1. Receive issue report
2. Log in ticketing system
3. Classify priority (P1-P4)
4. Attempt resolution within authority

**Step 2: First Escalation (L1)**
Escalate to Team Lead when:
- Resolution exceeds L0 authority
- Customer requests supervisor
- SLA at risk
- Policy clarification needed

**Step 3: Manager Escalation (L2)**
Escalate to Manager when:
- L1 cannot resolve within SLA
- Exception approval required
- Customer escalates further
- Financial impact > SGD 1,000

**Step 4: Director Escalation (L3)**
Escalate to Director when:
- L2 cannot resolve
- Financial impact > SGD 10,000
- Legal/compliance concern
- Key account at risk

**Step 5: Executive Escalation (L4)**
Escalate to MD when:
- Reputational risk
- Financial impact > SGD 50,000
- Regulatory investigation
- Media inquiry

---

## 6. Response Time by Level

| Level | Response Time | Update Frequency |
|-------|---------------|------------------|
| **L0** | Immediate | N/A |
| **L1** | 30 minutes | Every 2 hours |
| **L2** | 1 hour | Every 4 hours |
| **L3** | 2 hours | Twice daily |
| **L4** | 4 hours | Daily |

---

## 7. Escalation by Issue Type

### 7.1 Operational Issues

| Issue | Initial Level | Max Escalation |
|-------|---------------|----------------|
| Booking error | L0 | L2 |
| Documentation error | L0 | L2 |
| Shipment delay | L0 | L3 |
| Cargo damage | L1 | L3 |
| Cargo loss | L2 | L4 |
| Customs hold | L1 | L3 |

### 7.2 Customer Complaints

| Complaint Type | Initial Level | Max Escalation |
|----------------|---------------|----------------|
| Service quality | L0 | L2 |
| Billing dispute | L0 | L2 |
| Rate disagreement | L1 | L3 |
| Contract breach claim | L2 | L4 |
| Legal threat | L3 | L4 |

### 7.3 System/Technical Issues

| Issue | Initial Level | Max Escalation |
|-------|---------------|----------------|
| System slow | L0 (IT) | L2 |
| Feature not working | L1 (IT) | L2 |
| System down | L2 (IT) | L3 |
| Data breach | L3 | L4 |

---

## 8. Communication Protocol

### 8.1 Internal Communication

| Escalation | Communication Method |
|------------|---------------------|
| L0 → L1 | Direct approach, phone, or chat |
| L1 → L2 | Email with ticket reference |
| L2 → L3 | Email + phone call |
| L3 → L4 | Direct phone + written brief |

### 8.2 Escalation Email Template

```
Subject: [PRIORITY] Escalation - [Ticket#] - [Brief Description]

Dear [Name],

I am escalating the following issue that requires your attention:

**Ticket Number:** [#####]
**Customer:** [Customer Name]
**Issue Summary:** [One sentence]
**Priority:** [P1/P2/P3/P4]
**SLA Status:** [Time remaining / Breached]

**Background:**
[2-3 sentences on the issue]

**Actions Taken:**
1. [Action 1]
2. [Action 2]

**Current Blocker:**
[Why escalation is needed]

**Recommended Action:**
[What you need from escalation recipient]

**Customer Expectation:**
[What customer is expecting]

Please advise on the way forward.

Regards,
[Your Name]
```

### 8.3 Customer Communication

| Stage | Communication |
|-------|---------------|
| Issue received | Acknowledge with ticket number |
| Escalated | Inform customer of escalation |
| Status update | Per SLA update frequency |
| Resolution | Confirm resolution and close |
| Follow-up | Satisfaction check within 48 hours |

---

## 9. Escalation Contacts

### 9.1 Operations Escalation Matrix

| Time | L1 | L2 | L3 |
|------|----|----|-----|
| Office hours | Team Lead | Ops Manager | Ops Director |
| After hours | On-call supervisor | Duty Manager | On-call Director |
| Weekends | On-call supervisor | Duty Manager | On-call Director |

### 9.2 Emergency Contacts

| Role | Contact | Availability |
|------|---------|--------------|
| Duty Manager | +65 6234 5678 | 24/7 |
| On-call Director | +65 6234 5678 | 24/7 |
| Managing Director | Via Duty Manager | Critical only |

---

## 10. De-escalation

### 10.1 De-escalation Criteria

Issue can be de-escalated when:
- Root cause identified and contained
- Resolution plan agreed with customer
- No further senior intervention needed
- SLA recovery possible

### 10.2 De-escalation Process

1. Confirm resolution path with current level
2. Document resolution plan
3. Communicate to customer
4. Return ownership to appropriate level
5. Monitor until closed

---

## 11. Post-Escalation Review

### 11.1 Required for All P1/P2 Escalations

| Review Element | Timeline |
|----------------|----------|
| Incident report | Within 24 hours of resolution |
| Root cause analysis | Within 5 days |
| Preventive actions | Within 10 days |
| Management review | Monthly |

### 11.2 Incident Report Contents

- Incident timeline
- Root cause
- Impact assessment
- Resolution actions
- Preventive measures
- Lessons learned

---

## 12. Metrics and Reporting

### 12.1 Escalation KPIs

| Metric | Target |
|--------|--------|
| L1 resolution rate | > 80% |
| Average escalation level | < 1.5 |
| Escalation response time | Within SLA |
| Repeat escalations | < 5% |

### 12.2 Reporting Frequency

| Report | Frequency | Audience |
|--------|-----------|----------|
| Escalation log | Daily | Team Leads |
| Escalation summary | Weekly | Managers |
| Trend analysis | Monthly | Directors |
| Executive summary | Quarterly | MD |

---

*Procedure Owner: Operations Director*
*Next Review: July 1, 2025*
