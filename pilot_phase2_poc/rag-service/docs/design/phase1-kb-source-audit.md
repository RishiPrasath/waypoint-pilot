# Phase 1 Knowledge Base Source Audit

Status: Historical candidate audit complete; specialist promotion review still
required by `RAG-DT024`
Date: 2026-07-16
Task: `RAG-DT002`
Audit root: `legacy/phase1-kb-snapshot/`

## Scope and method

This audit covers the legacy Phase 1 snapshot only. It is an assessment of
candidate material, not a promotion decision. No file under `legacy/` is
canonical Phase 2 content until it passes the source-registry and materialization
gates in DT003, DT004, DT008, and DT012.

Inventory was performed by extension, directory, filename, and frontmatter/
provenance signals. The snapshot contains 82 Markdown files and 52 PDFs:

| Area | Markdown | PDF | Treatment |
|---|---:|---:|---|
| Regulatory | 46 | 33 | Authority review and source deduplication required |
| Carriers | 19 | 13 | Operational reference only; carrier authority/freshness review required |
| Reference | 9 | 6 | Reference material; verify edition and primary source |
| Internal synthetic | 7 | 0 | Synthetic internal-policy candidates; owner approval required |

The Markdown inventory found frontmatter in 81 of 82 files and URL signals in
39 files. These signals are useful for triage but do not prove source authority,
currentness, or safe promotion.

## Audit fields and decision vocabulary

Each source is assigned a stable source ID, legacy path, source type, authority
class, target status, blocker, next action, and priority. These fields are the
minimum contract for the source registry design.

Target statuses:

- `audit-only`: retained for traceability; not eligible for ingestion yet.
- `candidate`: potentially useful but requires authority, freshness, or content review.
- `promote-after-review`: structurally suitable once the named blocker is resolved.
- `exclude-or-replace`: duplicate, derivative, stale, marketing-heavy, or otherwise unsuitable.

Priority is `P0` for regulatory material needed to establish a safe first KB,
`P1` for useful secondary/reference material, and `P2` for optional or internal
material.

## Category decisions

| Source group | Source type | Authority | Target status | Blocker | Next action | Priority |
|---|---|---|---|---|---|---|
| Singapore regulatory Markdown | public_regulatory | Singapore Customs or stated public authority; verify per file | promote-after-review | source URL, date, and duplicate checks | DT003/DT008 registry review | P0 |
| ASEAN/regional regulatory Markdown | public_regulatory | ASEAN/WCO/other stated authority; verify per file | candidate | jurisdiction and edition validation | DT003 authority review | P0 |
| Regulatory PDF-derived Markdown | public_regulatory_candidate | original PDF authority not yet normalized | candidate | PDF/Markdown pairing and extraction fidelity | DT012 snapshot/materialization review | P0 |
| Carrier summaries and guides | public_carrier_candidate | carrier or secondary summary; not assumed authoritative | audit-only by default | carrier ownership, currentness, marketing content, and Phase 2 use-case fit | exclude marketing; promote static guidance only after explicit use-case approval | P1 |
| HS/Incoterms reference | public_reference | WCO, Singapore Customs, ICC, or stated publisher | candidate | edition/date and primary-source verification | DT003/DT012 review | P1 |
| Synthetic internal procedures/policies | synthetic_internal | internal product owner, not public authority | candidate | owner approval, version, and policy scope | separate namespace and approval | P2 |
| Snapshot README and generated derivatives | metadata_or_derivative | repository metadata, not domain authority | audit-only or exclude-or-replace | not a knowledge source | preserve for audit trail only | P2 |

## Source manifest

The following manifest accounts for every Markdown file in the audit root. The
default decision is intentionally conservative and must be refined by the
source registry task.

### Regulatory sources

| ID | Legacy path | Source type | Authority | Target status | Blocker | Next action | Priority |
|---|---|---|---|---|---|---|---|
| REG-001 | `01_regulatory/asean_rules_of_origin.md` | public_regulatory | ASEAN; verify primary source | candidate | authority/date | validate registry metadata | P0 |
| REG-002 | `01_regulatory/asean_tariff_finder_guide.md` | public_regulatory | ASEAN; verify primary source | candidate | authority/date | validate edition | P0 |
| REG-003 | `01_regulatory/atiga_overview.md` | public_regulatory | ASEAN | promote-after-review | URL/date | confirm current text | P0 |
| REG-004 | `01_regulatory/indonesia_import_requirements.md` | public_regulatory | Indonesia authority; verify | candidate | authority/date | validate jurisdiction | P0 |
| REG-005 | `01_regulatory/malaysia_import_requirements.md` | public_regulatory | Malaysia authority; verify | candidate | authority/date | validate jurisdiction | P0 |
| REG-006 | `01_regulatory/philippines_import_requirements.md` | public_regulatory | Philippines authority; verify | candidate | authority/date | validate jurisdiction | P0 |
| REG-007 | `01_regulatory/sg_certificates_of_origin.md` | public_regulatory | Singapore Customs; verify | promote-after-review | URL/date | confirm current procedure | P0 |
| REG-008 | `01_regulatory/sg_export_procedures.md` | public_regulatory | Singapore Customs; verify | promote-after-review | URL/date | confirm current procedure | P0 |
| REG-009 | `01_regulatory/sg_free_trade_zones.md` | public_regulatory | Singapore Customs; verify | promote-after-review | URL/date | confirm current procedure | P0 |
| REG-010 | `01_regulatory/sg_gst_guide.md` | public_regulatory | Singapore Customs/IRAS; verify | promote-after-review | URL/date | confirm current tax guidance | P0 |
| REG-011 | `01_regulatory/sg_hs_classification.md` | public_regulatory | Singapore Customs; verify | promote-after-review | URL/date | confirm current guidance | P0 |
| REG-012 | `01_regulatory/sg_import_procedures.md` | public_regulatory | Singapore Customs; verify | promote-after-review | URL/date | confirm current procedure | P0 |
| REG-013 | `01_regulatory/thailand_import_requirements.md` | public_regulatory | Thailand authority; verify | candidate | authority/date | validate jurisdiction | P1 |
| REG-014 | `01_regulatory/vietnam_import_requirements.md` | public_regulatory | Vietnam authority; verify | candidate | authority/date | validate jurisdiction | P1 |
| REG-015 | `01_regulatory/pdfs/aec_2025_trade_facilitation_sap.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-016 | `01_regulatory/pdfs/ahtn_2022_changes.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-017 | `01_regulatory/pdfs/asean_import_licensing_guidelines.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-018 | `01_regulatory/pdfs/asean_ntm_guidelines.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-019 | `01_regulatory/pdfs/asean_seamless_trade_facilitation_astfi.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition/size | DT012 verify and normalize | P0 |
| REG-020 | `01_regulatory/pdfs/asean_tariff_finder_leaflet.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-021 | `01_regulatory/pdfs/asean_trade_facilitation_framework.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-022 | `01_regulatory/pdfs/atiga_annex3_psr_hs2022.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-023 | `01_regulatory/pdfs/atiga_annex5_rvc_guidelines.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-024 | `01_regulatory/pdfs/atiga_annex6_partial_cumulation.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-025 | `01_regulatory/pdfs/atiga_annex7_form_d.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-026 | `01_regulatory/pdfs/atiga_annex8_awsc_ocp.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-027 | `01_regulatory/pdfs/atiga_fact_sheet_wto.md` | public_regulatory_candidate | WTO/ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-028 | `01_regulatory/pdfs/atiga_first_protocol_amendment.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-029 | `01_regulatory/pdfs/atiga_full_text.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-030 | `01_regulatory/pdfs/atiga_psr_implementing_guidelines.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-031 | `01_regulatory/pdfs/average_cept_atiga_tariff_rates.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-032 | `01_regulatory/pdfs/awsc_guidebook_english.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-033 | `01_regulatory/pdfs/awsc_origin_declaration_format.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-034 | `01_regulatory/pdfs/customs_guide_records_image_system.md` | public_regulatory_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-035 | `01_regulatory/pdfs/eform_d_full_implementation.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-036 | `01_regulatory/pdfs/ftz_circular_01_2020.md` | public_regulatory_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-037 | `01_regulatory/pdfs/general_interpretative_rules.md` | public_regulatory_candidate | WCO/Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-038 | `01_regulatory/pdfs/handbook_non_preferential_roo.md` | public_regulatory_candidate | ASEAN/WCO; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-039 | `01_regulatory/pdfs/handbook_roo_preferential_co.md` | public_regulatory_candidate | ASEAN/WCO; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-040 | `01_regulatory/pdfs/how_to_determine_hs_code.md` | public_regulatory_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-041 | `01_regulatory/pdfs/how_to_read_the_hs.md` | public_regulatory_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-042 | `01_regulatory/pdfs/minor_discrepancies_proof_of_origin.md` | public_regulatory_candidate | ASEAN; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-043 | `01_regulatory/pdfs/sg_customs_asean_aeo_mra.md` | public_regulatory_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-044 | `01_regulatory/pdfs/sg_customs_handbook_co_tradenet.md` | public_regulatory_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-045 | `01_regulatory/pdfs/sg_customs_important_permit_fields.md` | public_regulatory_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-046 | `01_regulatory/pdfs/sg_customs_mra_factsheet_asean.md` | public_regulatory_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P0 |
| REG-047 | `01_regulatory/pdfs/asean_self_certification_guidebook.pdf` | public_regulatory_candidate | ASEAN; no extracted Markdown candidate | audit-only | PDF-only source; provenance/edition/extraction not reviewed | DT012 extract, verify, and assign canonical candidate | P0 |

The `01_regulatory/pdfs/*.md` group contains: `aec_2025_trade_facilitation_sap`,
`ahtn_2022_changes`, `asean_import_licensing_guidelines`,
`asean_ntm_guidelines`, `asean_seamless_trade_facilitation_astfi`,
`asean_tariff_finder_leaflet`, `asean_trade_facilitation_framework`,
`atiga_annex3_psr_hs2022`, `atiga_annex5_rvc_guidelines`,
`atiga_annex6_partial_cumulation`, `atiga_annex7_form_d`,
`atiga_annex8_awsc_ocp`, `atiga_fact_sheet_wto`, `atiga_first_protocol_amendment`,
`atiga_full_text`, `atiga_psr_implementing_guidelines`,
`average_cept_atiga_tariff_rates`, `awsc_guidebook_english`,
`awsc_origin_declaration_format`, `customs_guide_records_image_system`,
`eform_d_full_implementation`, `ftz_circular_01_2020`,
`general_interpretative_rules`, `handbook_non_preferential_roo`,
`handbook_roo_preferential_co`, `how_to_determine_hs_code`,
`how_to_read_the_hs`, `minor_discrepancies_proof_of_origin`,
`sg_customs_asean_aeo_mra`, `sg_customs_handbook_co_tradenet`,
`sg_customs_important_permit_fields`, and `sg_customs_mra_factsheet_asean`.

### Carrier sources

| ID | Legacy path | Source type | Authority | Target status | Blocker | Next action | Priority |
|---|---|---|---|---|---|---|---|
| CAR-001 | `02_carriers/cathay_cargo_service_guide.md` | public_carrier_candidate | Cathay Cargo; source URL/version not recorded | audit-only | no confirmed static-carrier use case; provenance/freshness | exclude unless approved use case and authority evidence | P1 |
| CAR-002 | `02_carriers/evergreen_service_summary.md` | public_carrier_candidate | Evergreen; source URL/version not recorded | audit-only | summary/marketing risk; provenance/freshness | exclude unless approved use case and authority evidence | P1 |
| CAR-003 | `02_carriers/maersk_service_summary.md` | public_carrier_candidate | Maersk; source URL/version not recorded | audit-only | summary/marketing risk; provenance/freshness | exclude unless approved use case and authority evidence | P1 |
| CAR-004 | `02_carriers/one_service_summary.md` | public_carrier_candidate | ONE; source URL/version not recorded | audit-only | summary/marketing risk; provenance/freshness | exclude unless approved use case and authority evidence | P1 |
| CAR-005 | `02_carriers/pil_service_summary.md` | public_carrier_candidate | PIL; source URL/version not recorded | audit-only | summary/marketing risk; provenance/freshness | exclude unless approved use case and authority evidence | P1 |
| CAR-006 | `02_carriers/sia_cargo_service_guide.md` | public_carrier_candidate | SIA Cargo; source URL/version not recorded | audit-only | guide provenance/freshness; no confirmed use case | exclude unless approved use case and authority evidence | P1 |
| CAR-007 | `02_carriers/pdfs/maersk_sg_booking_amendment.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-008 | `02_carriers/pdfs/maersk_sg_demurrage_detention_calc.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-009 | `02_carriers/pdfs/maersk_sg_demurrage_detention.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-010 | `02_carriers/pdfs/maersk_sg_import_delivery_order.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-011 | `02_carriers/pdfs/maersk_sg_notifications_guide.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-012 | `02_carriers/pdfs/maersk_sg_shipping_instructions_guide.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-013 | `02_carriers/pdfs/maersk_sg_shipping_instructions.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-014 | `02_carriers/pdfs/maersk_sg_spot_booking_guide.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-015 | `02_carriers/pdfs/maersk_sg_spot_booking.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-016 | `02_carriers/pdfs/maersk_sg_telex_release_template.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-017 | `02_carriers/pdfs/maersk_sg_telex_release.md` | public_carrier_candidate | Maersk; original PDF/source must be verified | audit-only | PDF fidelity, provenance, freshness, use-case fit | DT012 review; promote only approved static guidance | P1 |
| CAR-018 | `02_carriers/pdfs/sia_cargo_thrucool_brochure.md` | public_carrier_candidate | SIA Cargo; original PDF/source must be verified | audit-only | marketing/brochure risk; provenance/freshness | exclude unless approved use case and authority evidence | P1 |
| CAR-019 | `02_carriers/pdfs/sia_cargo_thrufresh_brochure.md` | public_carrier_candidate | SIA Cargo; original PDF/source must be verified | audit-only | marketing/brochure risk; provenance/freshness | exclude unless approved use case and authority evidence | P1 |

The original PDFs paired with CAR-007 through CAR-019 are separate audit inputs;
each must retain the same source ID as its extracted Markdown candidate.

### Reference sources

| ID | Legacy path | Source type | Authority | Target status | Blocker | Next action | Priority |
|---|---|---|---|---|---|---|---|
| REF-001 | `03_reference/hs_code_structure_guide.md` | public_reference | Verify Singapore Customs/WCO | candidate | edition/source | validate primary source | P1 |
| REF-002 | `03_reference/incoterms_2020_reference.md` | public_reference | ICC; verify licensing/source | candidate | edition/source | validate reference use | P1 |
| REF-003 | `03_reference/incoterms_comparison_chart.md` | public_reference | Secondary/reference; verify | candidate | authority/licensing | retain only if sourced | P1 |
| REF-004 | `03_reference/pdfs/sg_customs_ahtn_2022_changes.md` | public_reference_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P1 |
| REF-005 | `03_reference/pdfs/sg_customs_gir.md` | public_reference_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P1 |
| REF-006 | `03_reference/pdfs/sg_customs_how_to_determine_hs_code.md` | public_reference_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P1 |
| REF-007 | `03_reference/pdfs/sg_customs_how_to_read_hs.md` | public_reference_candidate | Singapore Customs; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P1 |
| REF-008 | `03_reference/pdfs/wco_hs_compendium_30years.md` | public_reference_candidate | WCO; verify original | candidate | PDF provenance/edition/age | DT012 verify and normalize | P1 |
| REF-009 | `03_reference/pdfs/wco_understanding_hs_2028.md` | public_reference_candidate | WCO; verify original | candidate | PDF provenance/edition | DT012 verify and normalize | P1 |

The PDF group contains Singapore Customs HS/AHTN/GIR guidance and WCO HS
reference material.

### Synthetic internal sources

| ID | Legacy path | Source type | Authority | Target status | Blocker | Next action | Priority |
|---|---|---|---|---|---|---|---|
| INT-001 | `04_internal_synthetic/booking_procedure.md` | synthetic_internal | Internal policy candidate | candidate | owner/version approval | separate internal namespace | P2 |
| INT-002 | `04_internal_synthetic/cod_procedure.md` | synthetic_internal | Internal policy candidate | candidate | owner/version approval | separate internal namespace | P2 |
| INT-003 | `04_internal_synthetic/customer_faq.md` | synthetic_internal | Internal policy candidate | candidate | owner/version approval | separate internal namespace | P2 |
| INT-004 | `04_internal_synthetic/escalation_procedure.md` | synthetic_internal | Internal policy candidate | candidate | owner/version approval | separate internal namespace | P2 |
| INT-005 | `04_internal_synthetic/fta_comparison_matrix.md` | synthetic_internal | Internal reference candidate | candidate | owner/version approval | validate source basis | P2 |
| INT-006 | `04_internal_synthetic/service_terms_conditions.md` | synthetic_internal | Internal policy candidate | candidate | owner/version approval | separate internal namespace | P2 |
| INT-007 | `04_internal_synthetic/sla_policy.md` | synthetic_internal | Internal policy candidate | candidate | owner/version approval | separate internal namespace | P2 |

### Metadata and derivative files

| ID | Legacy path | Source type | Authority | Target status | Blocker | Next action | Priority |
|---|---|---|---|---|---|---|---|
| META-001 | `README.md` | metadata | Repository metadata | audit-only | not domain content | retain as snapshot documentation | P2 |

PDF files without a separately listed Markdown row remain paired audit inputs;
they must be checked for extraction fidelity and provenance before any Markdown
candidate is promoted. Duplicate PDF/Markdown pairs must resolve to one
canonical source record, not two ingestion records.

All regulatory and reference PDF candidates now have one source row. Original
PDFs must retain the same source ID as their extracted Markdown candidate.

## Phase 2 source boundary

`partner-source` is authoritative for live and operational shipment facts:
orders, current status, assignments, timelines, delivery events, and related
operational updates. Carrier documents must not answer order status, assignment,
ETA, timeline, or delivery-event questions. Those questions must be routed to
`partner-source` through the future BFF/orchestration layer.

Carrier material is not currently a required Phase 2 RAG source. It remains in
the audit for traceability and may be promoted only when all of the following
are true:

- a confirmed Phase 2 use case requires static carrier-specific guidance;
- the original carrier authority and current version are verified;
- citation and provenance are recorded;
- the source is placed in a separate `carrier_reference` namespace; and
- the source is marked non-authoritative for operational questions.

Carrier marketing brochures and generic service summaries should be excluded or
replaced unless a specific approved use case justifies them.

## Promotion rules and risks

1. A source requires a stable ID, title, authority, jurisdiction, source URL or
   documented acquisition path, snapshot date, and review owner before promotion.
2. Public regulatory content must be checked against the primary authority and
   current edition before it is used for operational answers.
3. Carrier content is scoped operational reference and must not override public
   regulatory authority.
4. Synthetic internal content requires an owner, version, effective date, and
   explicit namespace/priority rules before ingestion.
5. PDF-derived Markdown must be compared with its PDF and deduplicated before
   canonicalization.
6. Missing provenance, stale editions, extraction defects, and unresolved
   contradictions are blockers, not reasons to silently promote content.
7. Legacy carrier content defaults to non-retrieval-eligible until the carrier
   boundary and promotion conditions above are satisfied.

## Outputs and downstream impact

This audit unblocks source-registry design but does not authorize ingestion.

- DT003: use the candidate groups and authority-review rules to build the APAC
  source registry; decide whether any carrier reference sources are needed.
- DT004: keep legacy material outside active `knowledge_base/` until promotion.
- DT008: encode the required audit fields and statuses in the registry schema.
- DT012: define PDF snapshot and canonical Markdown handling.
- DT006/DT007: encode carrier-reference use cases separately from partner-source
  operational routing and negative cases.
- BT008/BT009/BT012: consume only explicitly promoted sources and resolved
  metadata.
- BT013/BT019: preserve source IDs and provenance for retrieval and evaluation.

## Verification summary

- Audit root confirmed: `legacy/phase1-kb-snapshot/`.
- Inventory confirmed: 82 Markdown files and 52 PDFs.
- Category counts recorded for regulatory, carrier, reference, and synthetic
  internal material.
- No file was moved or copied into the active `knowledge_base/`.
- All source groups have an explicit target status, blocker, next action, and
  priority.
