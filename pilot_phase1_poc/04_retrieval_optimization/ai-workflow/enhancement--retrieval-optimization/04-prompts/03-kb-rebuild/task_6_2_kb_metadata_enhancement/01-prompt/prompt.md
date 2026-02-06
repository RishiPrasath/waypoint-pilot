# Task 7.2: KB Metadata Enhancement (Retrieval Keywords + Body Terms)

## Persona

You are a knowledge base optimization specialist. Your job is to add retrieval-friendly metadata and synonym coverage to 30 markdown documents in a logistics RAG knowledge base. You understand that in this system, **only document body text gets embedded** — frontmatter is stripped before chunking. Therefore, the primary fix is injecting a "Key Terms and Abbreviations" section into each document's body so that abbreviations and synonyms become vector-searchable.

## Context

### The Problem

The Waypoint KB has 30 documents. The ingestion pipeline works like this:

```
Markdown file → process_docs.py (strips frontmatter) → chunker.py (splits body into ~600-char chunks) → ingest.py (embeds chunk_text via all-MiniLM-L6-v2) → ChromaDB
```

**Only `chunk_text` (body content) gets embedded.** Frontmatter fields like `retrieval_keywords` are NOT embedded and NOT even stored in ChromaDB currently.

The embedding model `all-MiniLM-L6-v2` does NOT know that:
- "BL" = "Bill of Lading"
- "D&D" = "Demurrage and Detention"  
- "CO" = "Certificate of Origin"
- "duty rate" ≈ "tariff"
- "SI" = "Shipping Instructions"

When customer service agents query using abbreviations (which they do constantly), the vector similarity is too low to retrieve the correct documents.

### The Solution

For each document, make exactly **2 changes**:

1. **Frontmatter**: Add `retrieval_keywords` list (for tracking/audit, future hybrid search)
2. **Body**: Insert a "Key Terms and Abbreviations" table immediately after the `# Title` heading, before the first `## Section`. This is what actually fixes retrieval.

### What NOT to Change

- Do NOT modify any existing body content (sections, tables, text)
- Do NOT reorder existing sections
- Do NOT change any existing frontmatter fields
- Do NOT touch files in `pdfs/` subdirectories
- Only ADD the `retrieval_keywords` field and the Key Terms section

## Task

### Phase 1: Process 22 Documents Missing Keywords

These documents have NO `retrieval_keywords` in frontmatter and NO Key Terms section in body. Add both.

**Working directory**: `pilot_phase1_poc/04_retrieval_optimization/kb/`

#### 01_regulatory (12 documents)

**File: `01_regulatory/sg_certificates_of_origin.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - CO
  - certificate of origin
  - Form D
  - preferential CO
  - non-preferential CO
  - ATIGA
  - self-certification
  - AWSC
  - back-to-back CO
  - third party invoicing
  - origin declaration
  - OD
  - proof of origin
  - ROO
  - rules of origin
```

Body — insert after `# ...` title, before first `## ...` section:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **CO** | Certificate of Origin | Document proving goods originate from a specific country |
| **Form D** | ATIGA Certificate of Origin | Preferential CO for ASEAN-ASEAN trade under ATIGA |
| **AWSC** | ASEAN-Wide Self-Certification | Certified Exporter issues own origin declaration |
| **OD** | Origin Declaration | Self-certified statement of origin on commercial docs |
| **ROO** | Rules of Origin | Criteria determining country of origin for tariff preference |
| **RVC** | Regional Value Content | Percentage of value originating in ASEAN (threshold: 40%) |
| **CTC** | Change in Tariff Classification | ROO method based on HS code change during manufacturing |
| **PCO** | Preferential Certificate of Origin | CO qualifying for reduced duty under FTA |
| **NPCO** | Non-Preferential Certificate of Origin | CO for non-tariff purposes (anti-dumping, quotas) |
```

---

**File: `01_regulatory/asean_rules_of_origin.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - rules of origin
  - ROO
  - RVC
  - regional value content
  - CTC
  - change in tariff classification
  - cumulation
  - ATIGA
  - Form D
  - wholly obtained
  - substantial transformation
  - de minimis
  - direct consignment
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **ROO** | Rules of Origin | Criteria determining where goods originate for FTA eligibility |
| **RVC** | Regional Value Content | Value-added threshold (typically 40% under ATIGA) |
| **CTC** | Change in Tariff Classification | Origin criterion based on HS code change |
| **CTH** | Change in Tariff Heading | CTC at 4-digit HS level |
| **CTSH** | Change in Tariff Sub-Heading | CTC at 6-digit HS level |
| **PSR** | Product Specific Rules | Origin rules for individual HS codes |
| **WO** | Wholly Obtained | Goods entirely produced in one country |
| **FOB** | Free on Board | Basis for RVC calculation (FOB price) |
| **Form D** | ATIGA Certificate of Origin | Preferential CO for intra-ASEAN trade |
```

---

**File: `01_regulatory/indonesia_import_requirements.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Indonesia import
  - INSW
  - Indonesia National Single Window
  - LARTAS
  - restricted goods
  - SNI
  - halal certification
  - API
  - importer identification number
  - Bea Cukai
  - customs clearance Indonesia
  - de minimis
  - PIB
  - import declaration
  - VAT Indonesia
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **INSW** | Indonesia National Single Window | Online portal for import/export permits and declarations |
| **LARTAS** | Larangan dan Pembatasan | Restricted and prohibited goods requiring special permits |
| **SNI** | Standar Nasional Indonesia | Mandatory product certification for 130+ categories |
| **API** | Angka Pengenal Importir | Importer Identification Number (required for all imports) |
| **PIB** | Pemberitahuan Impor Barang | Import Declaration Form submitted to Bea Cukai |
| **BPOM** | Badan Pengawas Obat dan Makanan | Food & drug regulatory agency (approvals for F&B, cosmetics) |
| **OSS** | Online Single Submission | Business licensing system integrated with INSW |
| **NIB** | Nomor Induk Berusaha | Business Identification Number (replaces older licenses) |
```

---

**File: `01_regulatory/thailand_import_requirements.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Thailand import
  - Thai customs
  - BOI
  - Board of Investment
  - customs tariff Thailand
  - VAT Thailand
  - import license Thailand
  - Form D Thailand
  - TISI
  - Thai Industrial Standard
  - EEC
  - Eastern Economic Corridor
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **BOI** | Board of Investment | Grants tax incentives and import duty exemptions |
| **TISI** | Thai Industrial Standards Institute | Product certification body (mandatory for some imports) |
| **EEC** | Eastern Economic Corridor | Special economic zone with customs incentives |
| **VAT** | Value Added Tax | 7% standard rate on imports (calculated on CIF + duty) |
| **FDA** | Food and Drug Administration (Thai) | Regulates food, drugs, cosmetics, medical devices |
| **Form D** | ATIGA Certificate of Origin | For preferential duty under ASEAN-ASEAN trade |
| **Form AK** | AKFTA Certificate of Origin | For preferential duty under ASEAN-Korea FTA |
| **Form E** | ACFTA Certificate of Origin | For preferential duty under ASEAN-China FTA |
```

---

**File: `01_regulatory/vietnam_import_requirements.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Vietnam import
  - Vietnam customs
  - VNACCS
  - Vietnam Automated Cargo Clearance System
  - import duty Vietnam
  - VAT Vietnam
  - special consumption tax
  - C/O Vietnam
  - Vietnam National Single Window
  - VNSW
  - MIC
  - Ministry of Industry and Trade
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **VNACCS** | Vietnam Automated Cargo Clearance System | Electronic customs declaration platform |
| **VNSW** | Vietnam National Single Window | One-stop portal for trade documentation |
| **MOIT** | Ministry of Industry and Trade | Issues import licenses, manages trade policy |
| **SCT** | Special Consumption Tax | Excise tax on luxury goods, alcohol, tobacco |
| **VAT** | Value Added Tax | 10% standard rate (8% reduced for some goods) |
| **Form D** | ATIGA Certificate of Origin | For preferential duty under ASEAN-ASEAN trade |
| **Form E** | ACFTA Certificate of Origin | For preferential duty under ASEAN-China FTA |
| **C/O** | Certificate of Origin | Generic abbreviation used in Vietnamese trade docs |
```

---

**File: `01_regulatory/philippines_import_requirements.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Philippines import
  - BOC
  - Bureau of Customs Philippines
  - import duty Philippines
  - VAT Philippines
  - e2m
  - Electronic to Mobile
  - FDA Philippines
  - import assessment
  - customs clearance Philippines
  - ASEAN Single Window Philippines
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **BOC** | Bureau of Customs | Philippines customs authority managing imports |
| **e2m** | Electronic to Mobile | BOC electronic customs processing system |
| **FDA** | Food and Drug Administration (Philippines) | Regulates food, drugs, cosmetics, medical devices |
| **VAT** | Value Added Tax | 12% on imports (on CIF + duty + other charges) |
| **CAO** | Customs Administrative Order | Regulatory directives issued by BOC |
| **CPRS** | Client Profile Registration System | Importer registration with BOC |
| **Form D** | ATIGA Certificate of Origin | For preferential duty under ASEAN-ASEAN trade |
| **SGL** | Super Green Lane | Expedited clearance for accredited importers |
```

---

**File: `01_regulatory/malaysia_import_requirements.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Malaysia import
  - RMCD
  - Royal Malaysian Customs
  - MyTradeLink
  - import duty Malaysia
  - SST
  - sales and service tax
  - DFTZ
  - Digital Free Trade Zone
  - uCustoms
  - customs clearance Malaysia
  - ATIGA Malaysia
  - de minimis Malaysia
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **RMCD** | Royal Malaysian Customs Department | Customs authority managing imports/exports |
| **SST** | Sales and Service Tax | Replaced GST in 2018 (sales tax 5-10%, service tax 6-8%) |
| **DFTZ** | Digital Free Trade Zone | E-commerce hub facilitating cross-border SME trade |
| **uCustoms** | uCustoms System | Electronic customs declaration and processing platform |
| **ATA** | Admission Temporaire | Carnet for temporary import/export of goods |
| **LMW** | Licensed Manufacturing Warehouse | Duty-free zone for manufacturing operations |
| **FIZ** | Free Industrial Zone | Customs-exempt area for export-oriented manufacturing |
| **Form D** | ATIGA Certificate of Origin | For preferential duty under ASEAN-ASEAN trade |
```

---

**File: `01_regulatory/sg_free_trade_zones.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - FTZ
  - free trade zone
  - free trade zone Singapore
  - re-export
  - transshipment
  - bonded warehouse
  - GST suspension
  - zero GST
  - Jurong Port FTZ
  - Changi FTZ
  - Keppel FTZ
  - PSA FTZ
  - duty-free
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **FTZ** | Free Trade Zone | Designated area where GST is suspended on goods in transit |
| **GST** | Goods and Services Tax | 9% tax suspended for goods within FTZ until domestic entry |
| **3PL** | Third Party Logistics | Licensed 3PLs can qualify for GST suspension schemes |
| **ZGS** | Zero-GST Storage | Warehouse scheme for GST-suspended storage of imports |
| **IGDS** | Import GST Deferment Scheme | Defer GST payment from import to GST return filing |
| **PSA** | Port of Singapore Authority | Operates Singapore's container terminals |
| **NTP** | Networked Trade Platform | Singapore's one-stop trade and logistics ecosystem |
```

---

**File: `01_regulatory/asean_tariff_finder_guide.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - ASEAN Tariff Finder
  - tariff rate
  - duty rate
  - MFN
  - most favoured nation
  - preferential tariff
  - ATIGA tariff
  - RCEP tariff
  - FTA tariff lookup
  - tariff schedule
  - HS code tariff
  - customs duty
  - import duty
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **MFN** | Most Favoured Nation | Default (non-preferential) duty rate applied to WTO members |
| **ATIGA** | ASEAN Trade in Goods Agreement | FTA providing preferential tariffs within ASEAN |
| **RCEP** | Regional Comprehensive Economic Partnership | FTA covering ASEAN + 5 partners (China, Japan, Korea, Australia, NZ) |
| **ACFTA** | ASEAN-China FTA | Bilateral FTA with preferential rates for China-ASEAN trade |
| **AKFTA** | ASEAN-Korea FTA | Bilateral FTA with preferential rates for Korea-ASEAN trade |
| **AIFTA** | ASEAN-India FTA | Bilateral FTA with preferential rates for India-ASEAN trade |
| **HS** | Harmonized System | International 6-digit product classification for tariffs |
| **AHTN** | ASEAN Harmonized Tariff Nomenclature | ASEAN's 8-digit extension of the HS code |
```

---

**File: `01_regulatory/sg_export_procedures.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Singapore export
  - export permit
  - export declaration
  - TradeNet
  - strategic goods
  - controlled goods
  - OUT permit
  - customs export Singapore
  - record retention
  - export documentation Singapore
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **OUT permit** | Outward Declaration Permit | Required for goods leaving Singapore customs territory |
| **TradeNet** | TradeNet System | Singapore's electronic trade declaration system (since 1989) |
| **NTP** | Networked Trade Platform | One-stop digital trade platform replacing TradeNet frontend |
| **STP** | Strategic Trade Permit | Required for export of strategic/dual-use goods |
| **DA** | Declaring Agent | Licensed customs broker submitting permits on behalf of shippers |
| **CMP** | Customs Management of Permits | Compliance scheme for trusted traders |
| **SG** | Strategic Goods | Controlled items under Strategic Goods Control Act |
```

---

**File: `01_regulatory/sg_import_procedures.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Singapore import
  - import permit
  - import declaration
  - IN permit
  - TradeNet
  - GST import
  - IGDS
  - MES
  - Major Exporter Scheme
  - TIS
  - customs clearance Singapore
  - import documentation Singapore
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **IN permit** | Inward Declaration Permit | Required for goods entering Singapore customs territory |
| **TradeNet** | TradeNet System | Electronic trade declaration system for permit applications |
| **IGDS** | Import GST Deferment Scheme | Defer GST payment to monthly GST return (reduces cash flow impact) |
| **MES** | Major Exporter Scheme | GST suspension for qualifying exporters (>50% exports) |
| **TIS** | Temporary Import Scheme | Duty/GST suspension for goods imported temporarily |
| **NTP** | Networked Trade Platform | One-stop digital trade platform |
| **DA** | Declaring Agent | Licensed customs broker submitting permits |
| **FTZ** | Free Trade Zone | GST-suspended area; duty applies only on domestic entry |
```

---

**File: `01_regulatory/sg_gst_guide.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - GST
  - goods and services tax
  - import GST
  - GST rate Singapore
  - 9 percent
  - GST relief
  - GST refund
  - IGDS
  - MES
  - import tax Singapore
  - duty Singapore
  - customs duty Singapore
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **GST** | Goods and Services Tax | Singapore's consumption tax at 9% (since Jan 2024) |
| **IGDS** | Import GST Deferment Scheme | Defer import GST to monthly return instead of paying at import |
| **MES** | Major Exporter Scheme | GST suspension for businesses exporting >50% of goods |
| **IRAS** | Inland Revenue Authority of Singapore | Tax authority administering GST registration and refunds |
| **CIF** | Cost, Insurance and Freight | Basis for import GST calculation (CIF + duty + other charges) |
| **FTZ** | Free Trade Zone | Area where import GST is suspended until goods enter domestic market |
| **3PL** | Third Party Logistics (Approved Scheme) | GST suspension for qualifying logistics providers |
```

---

#### 02_carriers (6 documents)

**File: `02_carriers/maersk_service_summary.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Maersk
  - ocean freight
  - container shipping
  - BL
  - bill of lading
  - B/L
  - SI
  - shipping instructions
  - D&D
  - demurrage
  - detention
  - DO
  - delivery order
  - VGM
  - verified gross mass
  - telex release
  - FCL
  - LCL
  - reefer
  - spot booking
  - booking amendment
  - transit time
  - container tracking
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **BL / B/L** | Bill of Lading | Transport document issued by Maersk as carrier |
| **SI** | Shipping Instructions | Document submitted by shipper before vessel cutoff |
| **D&D** | Demurrage and Detention | Port storage charges (demurrage) + container usage charges (detention) |
| **DO** | Delivery Order | Release document for collecting import containers |
| **VGM** | Verified Gross Mass | SOLAS-mandated container weight declaration |
| **FCL** | Full Container Load | Dedicated container for single shipper |
| **LCL** | Less than Container Load | Consolidated cargo from multiple shippers |
| **LOI** | Letter of Indemnity | Required for telex release without original BL |
| **LOA** | Letter of Authorization | Required for agent-submitted delivery orders |
| **TEU** | Twenty-foot Equivalent Unit | Standard container size measurement |
| **EBL** | Electronic Bill of Lading | Digital BL via Maersk platform |
```

---

**File: `02_carriers/pil_service_summary.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - PIL
  - Pacific International Lines
  - ocean freight
  - BL
  - bill of lading
  - container shipping
  - intra-Asia
  - reefer
  - FCL
  - LCL
  - transit time
  - VGM
  - D&D
  - demurrage
  - detention
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **PIL** | Pacific International Lines | Singapore-headquartered ocean carrier |
| **BL / B/L** | Bill of Lading | Transport document issued by PIL as carrier |
| **SI** | Shipping Instructions | Document submitted before vessel cutoff |
| **D&D** | Demurrage and Detention | Storage and container usage charges |
| **VGM** | Verified Gross Mass | Container weight declaration (SOLAS requirement) |
| **FCL** | Full Container Load | Dedicated container shipment |
| **LCL** | Less than Container Load | Consolidated cargo |
| **TEU** | Twenty-foot Equivalent Unit | Container size measurement |
```

---

**File: `02_carriers/one_service_summary.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - ONE
  - Ocean Network Express
  - ocean freight
  - BL
  - bill of lading
  - container shipping
  - FCL
  - LCL
  - reefer
  - transit time
  - VGM
  - D&D
  - demurrage
  - detention
  - SI
  - shipping instructions
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **ONE** | Ocean Network Express | Carrier formed from merger of MOL, NYK, K Line container operations |
| **BL / B/L** | Bill of Lading | Transport document issued by ONE as carrier |
| **SI** | Shipping Instructions | Document submitted before vessel cutoff |
| **D&D** | Demurrage and Detention | Storage and container usage charges |
| **VGM** | Verified Gross Mass | Container weight declaration (SOLAS requirement) |
| **FCL** | Full Container Load | Dedicated container shipment |
| **LCL** | Less than Container Load | Consolidated cargo |
| **TEU** | Twenty-foot Equivalent Unit | Container size measurement |
```

---

**File: `02_carriers/evergreen_service_summary.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Evergreen
  - Evergreen Marine
  - ocean freight
  - BL
  - bill of lading
  - container shipping
  - FCL
  - LCL
  - reefer
  - transit time
  - VGM
  - D&D
  - demurrage
  - detention
  - ShipmentLink
  - tracking
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **BL / B/L** | Bill of Lading | Transport document issued by Evergreen as carrier |
| **SI** | Shipping Instructions | Document submitted before vessel cutoff |
| **D&D** | Demurrage and Detention | Storage and container usage charges |
| **VGM** | Verified Gross Mass | Container weight declaration (SOLAS requirement) |
| **FCL** | Full Container Load | Dedicated container shipment |
| **LCL** | Less than Container Load | Consolidated cargo |
| **TEU** | Twenty-foot Equivalent Unit | Container size measurement |
| **PSA** | Port of Singapore Authority | Terminal operator; Evergreen-PSA joint venture |
```

---

**File: `02_carriers/cathay_cargo_service_guide.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Cathay Cargo
  - Cathay Pacific
  - air freight
  - air cargo
  - AWB
  - air waybill
  - MAWB
  - HAWB
  - house air waybill
  - DG
  - dangerous goods
  - perishable
  - temperature controlled
  - air freight rate
  - transit time air
  - cargo tracking
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **AWB** | Air Waybill | Transport document for air cargo (equivalent of BL for sea) |
| **MAWB** | Master Air Waybill | AWB between airline and freight forwarder |
| **HAWB** | House Air Waybill | AWB between freight forwarder and shipper |
| **DG** | Dangerous Goods | Cargo requiring special handling per IATA DGR |
| **ULD** | Unit Load Device | Container or pallet for loading aircraft |
| **IATA DGR** | IATA Dangerous Goods Regulations | Rules governing air transport of hazardous materials |
| **SHC** | Special Handling Code | IATA codes indicating special cargo requirements (e.g., PER, DGR) |
| **e-AWB** | Electronic Air Waybill | Paperless AWB for streamlined processing |
```

---

**File: `02_carriers/sia_cargo_service_guide.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - SIA Cargo
  - Singapore Airlines Cargo
  - air freight
  - air cargo
  - AWB
  - air waybill
  - THRUCOOL
  - THRUFRESH
  - temperature controlled
  - perishable
  - DG
  - dangerous goods
  - pharmaceutical
  - express freight
  - cargo tracking
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **AWB** | Air Waybill | Transport document for air cargo |
| **MAWB** | Master Air Waybill | AWB between SIA Cargo and freight forwarder |
| **HAWB** | House Air Waybill | AWB between freight forwarder and shipper |
| **THRUCOOL** | THRUCOOL Service | SIA Cargo's temperature-controlled solution for pharma |
| **THRUFRESH** | THRUFRESH Service | SIA Cargo's cold chain solution for perishables |
| **DG** | Dangerous Goods | Cargo requiring special handling per IATA DGR |
| **ULD** | Unit Load Device | Container/pallet for aircraft loading |
| **SHC** | Special Handling Code | IATA codes for special cargo (PER, PIL, DGR, etc.) |
```

---

#### 03_reference (3 documents)

**File: `03_reference/hs_code_structure_guide.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - HS code
  - Harmonized System
  - tariff classification
  - product classification
  - GIR
  - General Interpretive Rules
  - AHTN
  - tariff heading
  - chapter
  - subheading
  - customs classification
  - WCO
  - how to classify
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **HS** | Harmonized System | International 6-digit product classification (WCO-maintained) |
| **AHTN** | ASEAN Harmonized Tariff Nomenclature | ASEAN's 8-digit extension of the HS code |
| **GIR** | General Interpretive Rules | 6 rules governing how to classify goods under HS |
| **WCO** | World Customs Organization | International body maintaining the HS system |
| **CTH** | Change in Tariff Heading | Classification change at 4-digit level (ROO criterion) |
| **CTSH** | Change in Tariff Sub-Heading | Classification change at 6-digit level |
| **BTN** | Brussels Tariff Nomenclature | Predecessor to the Harmonized System |
| **EN** | Explanatory Notes | Official WCO guidance on HS classification |
```

---

**File: `03_reference/incoterms_2020_reference.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Incoterms
  - Incoterms 2020
  - FOB
  - CIF
  - DDP
  - EXW
  - DAP
  - FCA
  - CFR
  - CPT
  - CIP
  - DPU
  - FAS
  - trade terms
  - shipping terms
  - delivery terms
  - risk transfer
  - cost transfer
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **FOB** | Free on Board | Seller delivers to vessel; risk transfers at ship's rail |
| **CIF** | Cost, Insurance and Freight | Seller pays freight + insurance to destination port |
| **EXW** | Ex Works | Buyer bears all costs and risk from seller's premises |
| **DDP** | Delivered Duty Paid | Seller bears all costs including import duty and taxes |
| **DAP** | Delivered at Place | Seller delivers to named place; buyer handles import clearance |
| **FCA** | Free Carrier | Seller delivers to carrier at named place |
| **CFR** | Cost and Freight | Seller pays freight to destination; risk transfers at origin |
| **CPT** | Carriage Paid To | Like CFR but for any transport mode |
| **CIP** | Carriage and Insurance Paid To | Like CIF but for any transport mode |
| **DPU** | Delivered at Place Unloaded | Seller delivers and unloads at named place |
| **FAS** | Free Alongside Ship | Seller delivers alongside vessel at port of shipment |
```

---

**File: `03_reference/incoterms_comparison_chart.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - Incoterms comparison
  - FOB vs CIF
  - EXW vs DDP
  - Incoterms chart
  - which Incoterm
  - cost responsibility
  - risk transfer point
  - Incoterms decision
  - shipping terms comparison
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **FOB** | Free on Board | Most common for sea freight; seller delivers to vessel |
| **CIF** | Cost, Insurance and Freight | Seller pays freight + insurance to destination |
| **EXW** | Ex Works | Minimum seller responsibility; buyer arranges everything |
| **DDP** | Delivered Duty Paid | Maximum seller responsibility; includes all duties/taxes |
| **DAP** | Delivered at Place | Seller delivers to destination; buyer clears customs |
| **FCA** | Free Carrier | Flexible term for any transport mode |
```

---

#### 04_internal_synthetic (1 document)

**File: `04_internal_synthetic/fta_comparison_matrix.md`**

Frontmatter — add:
```yaml
retrieval_keywords:
  - FTA
  - free trade agreement
  - FTA comparison
  - ATIGA
  - RCEP
  - ACFTA
  - AKFTA
  - AIFTA
  - AANZFTA
  - which FTA
  - preferential tariff
  - duty rate comparison
  - Form D
  - Form E
  - Form AK
  - Form AI
```

Body — insert after title:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **FTA** | Free Trade Agreement | Trade agreement providing preferential duty rates |
| **ATIGA** | ASEAN Trade in Goods Agreement | Intra-ASEAN FTA (Form D) |
| **RCEP** | Regional Comprehensive Economic Partnership | ASEAN+5 FTA (15 countries) |
| **ACFTA** | ASEAN-China FTA | Bilateral FTA (Form E) |
| **AKFTA** | ASEAN-Korea FTA | Bilateral FTA (Form AK) |
| **AIFTA** | ASEAN-India FTA | Bilateral FTA (Form AI) |
| **AANZFTA** | ASEAN-Australia-NZ FTA | Bilateral FTA (Form AANZ) |
| **MFN** | Most Favoured Nation | Default WTO duty rate (no FTA preference) |
| **ROO** | Rules of Origin | Criteria to qualify for preferential FTA rates |
```

---

### Phase 2: Verify 8 Documents With Existing Keywords

These documents already have `retrieval_keywords` in frontmatter. For each:
1. Read the document body
2. Check if the keywords from frontmatter actually appear in the body text
3. If there is NO "Key Terms and Abbreviations" section, add one using the same table format
4. If keywords only exist in frontmatter but not in body, the Key Terms section fixes this

**File: `01_regulatory/atiga_overview.md`** — Has keywords. Check body for Key Terms section. Add if missing.

Suggested Key Terms if missing:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **ATIGA** | ASEAN Trade in Goods Agreement | Legal framework for ASEAN free trade in goods |
| **Form D** | ATIGA Certificate of Origin | Preferential CO for intra-ASEAN trade |
| **RVC** | Regional Value Content | Origin criterion: minimum 40% ASEAN value added |
| **CTC** | Change in Tariff Classification | Origin criterion: HS code changes during production |
| **MFN** | Most Favoured Nation | Default (non-preferential) tariff rate |
| **CEPT** | Common Effective Preferential Tariff | ATIGA predecessor scheme |
| **AWSC** | ASEAN-Wide Self-Certification | Certified Exporters self-declare origin |
| **ATFF** | ASEAN Trade Facilitation Framework | Trade facilitation strategic framework |
```

**File: `01_regulatory/sg_hs_classification.md`** — Has keywords. Check body. Add Key Terms if missing.

Suggested Key Terms:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **HS** | Harmonized System | International product classification system |
| **AHTN** | ASEAN Harmonized Tariff Nomenclature | 8-digit ASEAN extension of HS |
| **GIR** | General Interpretive Rules | 6 rules for classifying goods |
| **EN** | Explanatory Notes | WCO's official classification guidance |
| **WCO** | World Customs Organization | Maintains the HS system |
```

**File: `04_internal_synthetic/booking_procedure.md`** — Has keywords. Check body. Add Key Terms if missing.

Suggested Key Terms:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **FCL** | Full Container Load | Dedicated container for one shipper |
| **LCL** | Less than Container Load | Shared container, consolidated cargo |
| **BL / B/L** | Bill of Lading | Transport document proving shipment contract |
| **SI** | Shipping Instructions | Document submitted before vessel cutoff |
| **VGM** | Verified Gross Mass | SOLAS-mandated container weight declaration |
| **OOG** | Out of Gauge | Oversized cargo requiring special equipment |
| **DG** | Dangerous Goods | Hazardous cargo requiring special documentation |
```

**File: `04_internal_synthetic/customer_faq.md`** — Has keywords. Check body. Add Key Terms if missing.

Suggested Key Terms:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **FCL** | Full Container Load | Whole container booked by one shipper |
| **LCL** | Less than Container Load | Shared container for smaller shipments |
| **BL** | Bill of Lading | Proof of shipment and title document |
| **ETA** | Estimated Time of Arrival | Expected arrival date at destination |
| **ETD** | Estimated Time of Departure | Expected departure date from origin |
```

**File: `04_internal_synthetic/service_terms_conditions.md`** — Has keywords. Check body. Add Key Terms if missing. **Also fix: replace all `[Company Name]` with `Waypoint Logistics Pte Ltd`**.

Suggested Key Terms:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **FCL** | Full Container Load | Dedicated container shipment |
| **LCL** | Less than Container Load | Consolidated cargo shipment |
| **BL** | Bill of Lading | Transport document and receipt for goods |
| **D2D** | Door-to-Door | Full-service including pickup, customs, delivery |
| **P2P** | Port-to-Port | Terminal-to-terminal service only |
| **COD** | Cash on Delivery | Payment collected at delivery |
```

**File: `04_internal_synthetic/sla_policy.md`** — Has keywords. Check body. Add Key Terms if missing. **Also fix: replace all `+65 XXXX XXXX` with `+65 6234 5678`**.

Suggested Key Terms:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **SLA** | Service Level Agreement | Guaranteed performance targets |
| **KPI** | Key Performance Indicator | Measurable metric for service quality |
| **TAT** | Turnaround Time | Time from request to completion |
| **OTIF** | On Time In Full | Delivery meeting both time and completeness targets |
| **POD** | Proof of Delivery | Signed confirmation of goods received |
```

**File: `04_internal_synthetic/cod_procedure.md`** — Has keywords. Check body. Add Key Terms if missing.

Suggested Key Terms:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **COD** | Cash/Collect on Delivery | Payment collected from consignee at delivery |
| **POD** | Proof of Delivery | Signed confirmation with payment receipt |
| **DO** | Delivery Order | Authorization for cargo release |
| **AR** | Accounts Receivable | Outstanding COD amounts pending remittance |
```

**File: `04_internal_synthetic/escalation_procedure.md`** — Has keywords. Check body. Add Key Terms if missing. **Also fix: replace all `+65 XXXX XXXX` with `+65 6234 5678`**.

Suggested Key Terms:
```markdown
## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **SLA** | Service Level Agreement | Target response/resolution times per severity |
| **P1 / P2 / P3** | Priority Levels | Severity classification for escalation routing |
| **TAT** | Turnaround Time | Maximum time allowed for each escalation tier |
| **CS** | Customer Service | First-line team handling initial queries |
| **OPS** | Operations | Second-line team for operational issues |
```

---

### Phase 3: Fix Placeholder Text

While editing the 3 documents above, also make these replacements:

**`04_internal_synthetic/service_terms_conditions.md`**:
- Replace ALL instances of `[Company Name]` with `Waypoint Logistics Pte Ltd`

**`04_internal_synthetic/sla_policy.md`**:
- Replace ALL instances of `+65 XXXX XXXX` with `+65 6234 5678`

**`04_internal_synthetic/escalation_procedure.md`**:
- Replace ALL instances of `+65 XXXX XXXX` with `+65 6234 5678`

---

### Phase 4: Validate

After all 30 documents are updated:

```bash
cd pilot_phase1_poc/04_retrieval_optimization
venv\Scripts\activate

# Re-ingest with clean slate
python scripts/ingest.py --clear

# Verify doc count (expect 30) and chunk count
python scripts/verify_ingestion.py

# Run retrieval quality test
python scripts/retrieval_quality_test.py
```

Compare results to Task 7 baseline. Append Round 2 results to `reports/03_retrieval_validation.md`.

**Target**: ≥88% adjusted hit rate.

---

## Format

### How to Edit Each Document

For each document, you need to make exactly 2 edits:

**Edit 1 — Frontmatter**: Find the closing `---` of the frontmatter block. Insert the `retrieval_keywords` field just before it. Example:

Before:
```yaml
use_cases: [UC-3.1, UC-3.2]
---
```

After:
```yaml
use_cases: [UC-3.1, UC-3.2]
retrieval_keywords:
  - keyword1
  - keyword2
---
```

**Edit 2 — Body Key Terms**: Find the `# Title` line. Find the next `## Section` line after it. Insert the Key Terms table between them.

Before:
```markdown
# Maersk Service Summary

## Company Overview
```

After:
```markdown
# Maersk Service Summary

## Key Terms and Abbreviations

| Abbreviation | Full Term | Context |
|:------------|:----------|:--------|
| **BL / B/L** | Bill of Lading | Transport document issued by Maersk as carrier |
...

## Company Overview
```

### Execution Order

Process documents in this order:
1. All 12 regulatory docs (01_regulatory/)
2. All 6 carrier docs (02_carriers/)
3. All 3 reference docs (03_reference/)
4. The 1 internal doc missing keywords (fta_comparison_matrix)
5. The 8 internal/regulatory docs needing verification + Key Terms
6. The 3 placeholder fixes
7. Run validation (Phase 4)

### Output

Save a summary report to:
```
04-prompts/03-kb-rebuild/task_7_2_kb_metadata_enhancement/02-output/REPORT.md
```

Report should include:
- Documents modified (count and list)
- Keywords added per document
- Key Terms rows added per document
- Placeholder fixes applied
- Validation results (before/after hit rates)
