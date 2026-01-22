---
title: HS Code Structure Guide
source_organization: World Customs Organization (WCO)
source_urls:
  - url: https://www.wcoomd.org/en/topics/nomenclature/overview.aspx
    description: WCO Nomenclature and Classification of Goods overview
    retrieved_date: 2025-01-22
  - url: https://www.wcoomd.org/en/topics/nomenclature/overview/what-is-the-harmonized-system.aspx
    description: What is the Harmonized System (HS)?
    retrieved_date: 2025-01-22
  - url: https://www.wcoomd.org/en/topics/nomenclature/overview/hs-multi-purposes-tool.aspx
    description: The HS as a multi-purpose tool for trade
    retrieved_date: 2025-01-22
source_type: public_regulatory
last_updated: 2025-01-22
jurisdiction: Global
category: reference
use_cases: [UC-1.3, UC-2.1, UC-2.2, UC-2.3]
---

# HS Code Structure Guide

## Overview

The Harmonized Commodity Description and Coding System, commonly known as the Harmonized System (HS), is an international nomenclature for the classification of products. It is maintained by the World Customs Organization (WCO) and used by more than 200 countries as the basis for customs tariffs and trade statistics.

### Purpose of HS Codes

- **Customs duties**: Determine applicable tariff rates
- **Trade statistics**: Track international trade flows
- **Trade agreements**: Define product coverage in FTAs
- **Regulatory compliance**: Identify controlled/restricted goods
- **Origin determination**: Apply rules of origin criteria

---

## HS Code Structure

### International Standard: 6 Digits

```
HS Code: 85.17.13

Section:    XVI (Machinery and Mechanical Appliances)
  │
Chapter:   85 (Electrical machinery and equipment)
  │         ├─ First 2 digits
  │
Heading:   85.17 (Telephone sets; cellular phones)
  │         ├─ First 4 digits
  │
Subheading: 8517.13 (Smartphones)
            ├─ First 6 digits (international standard)
```

### Extended Codes: 8-10 Digits

Countries extend the 6-digit HS code for more specific classification:

```
Singapore AHTN: 8517.13.00.00
                │      │  │  │
                │      │  │  └─ National subdivision (10th digit)
                │      │  └──── National subdivision (9th digit)
                │      └─────── AHTN subdivision (7-8th digits)
                └──────────────  HS subheading (6 digits)
```

---

## Hierarchical Structure

### Sections (21 total)

| Section | Description | Chapters |
|---------|-------------|----------|
| I | Live animals; animal products | 01-05 |
| II | Vegetable products | 06-14 |
| III | Fats and oils | 15 |
| IV | Food, beverages, tobacco | 16-24 |
| V | Mineral products | 25-27 |
| VI | Chemical products | 28-38 |
| VII | Plastics and rubber | 39-40 |
| VIII | Leather and articles | 41-43 |
| IX | Wood and articles | 44-46 |
| X | Paper and paperboard | 47-49 |
| XI | Textiles and articles | 50-63 |
| XII | Footwear, headgear | 64-67 |
| XIII | Stone, ceramics, glass | 68-70 |
| XIV | Precious metals, jewelry | 71 |
| XV | Base metals and articles | 72-83 |
| XVI | Machinery and equipment | 84-85 |
| XVII | Vehicles, aircraft, vessels | 86-89 |
| XVIII | Optical, medical, instruments | 90-92 |
| XIX | Arms and ammunition | 93 |
| XX | Miscellaneous manufactured | 94-96 |
| XXI | Works of art, antiques | 97 |

### Chapters (97 total)

Each section contains chapters (2-digit codes). Examples:

| Chapter | Description |
|---------|-------------|
| 01 | Live animals |
| 27 | Mineral fuels, oils |
| 39 | Plastics and articles thereof |
| 61 | Knitted apparel |
| 62 | Woven apparel |
| 84 | Nuclear reactors, boilers, machinery |
| 85 | Electrical machinery and equipment |
| 87 | Vehicles other than railway |

### Headings (4-digit)

Within each chapter, headings provide more specificity:

**Chapter 85 Example:**

| Heading | Description |
|---------|-------------|
| 85.01 | Electric motors and generators |
| 85.04 | Transformers, static converters |
| 85.17 | Telephone sets, smartphones |
| 85.23 | Discs, tapes, storage devices |
| 85.28 | Monitors and projectors |
| 85.42 | Electronic integrated circuits |

### Subheadings (6-digit)

Further breakdown within headings:

**Heading 85.17 Example:**

| Subheading | Description |
|------------|-------------|
| 8517.11 | Line telephone sets with cordless handsets |
| 8517.12 | Telephones for cellular networks (feature phones) |
| 8517.13 | Smartphones |
| 8517.14 | Other telephones |
| 8517.61 | Base stations |
| 8517.62 | Machines for reception/transmission |

---

## General Interpretive Rules (GIR)

The GIR are six rules that govern HS classification:

### Rule 1: Section/Chapter Notes
Classification is determined by the terms of headings and section/chapter notes.

### Rule 2: Incomplete/Unfinished Goods
(a) Incomplete articles classified as complete if they have essential character
(b) Mixtures and combinations - classify by constituent materials

### Rule 3: Two or More Headings Applicable
(a) **Most specific description** takes precedence
(b) **Essential character** for mixtures/composites
(c) **Last in numerical order** as tiebreaker

### Rule 4: Most Akin
Goods not classifiable under Rules 1-3 go to heading of most similar goods.

### Rule 5: Containers and Packing
(a) Cases/containers presented with goods - classify with goods
(b) Packing materials - classify with goods (unless clearly reusable)

### Rule 6: Subheading Classification
Rules 1-5 apply at subheading level; compare within same level.

---

## Classification Examples

### Example 1: Smartphone

```
Product: Apple iPhone

Step 1: Section - XVI (Machinery)
Step 2: Chapter - 85 (Electrical machinery)
Step 3: Heading - 85.17 (Telephones)
Step 4: Subheading - 8517.13 (Smartphones)

HS Code: 8517.13
Singapore: 8517.13.00.00
```

### Example 2: Laptop Computer

```
Product: Dell Laptop

Step 1: Section - XVI (Machinery)
Step 2: Chapter - 84 (Machinery, mechanical appliances)
Step 3: Heading - 84.71 (Automatic data processing machines)
Step 4: Subheading - 8471.30 (Portable, weight ≤10kg)

HS Code: 8471.30
Singapore: 8471.30.10.00 (laptops)
```

### Example 3: Cotton T-Shirt

```
Product: Men's cotton knitted T-shirt

Step 1: Section - XI (Textiles)
Step 2: Chapter - 61 (Knitted or crocheted apparel)
Step 3: Heading - 61.09 (T-shirts, singlets)
Step 4: Subheading - 6109.10 (Of cotton)

HS Code: 6109.10
Singapore: 6109.10.00.00
```

### Example 4: Multi-Function Device

```
Product: Printer/Scanner/Copier (MFD)

Classification Challenge: Multiple functions
Rule 3(b): Essential character determines classification

If primarily a printer → 8443.31 (printing machines)
If primarily a copier → 8443.39 (other office machines)

Typical classification: 8443.31 (if main use is printing)
```

---

## ASEAN Harmonised Tariff Nomenclature (AHTN)

### Structure

AHTN extends the 6-digit HS to 8 digits for ASEAN countries:

```
AHTN 2022: Based on HS 2022
Format:   XXXX.XX.XX
          │      │  │
          │      │  └─ AHTN split (7-8th digits)
          │      └──── HS subheading (5-6th digits)
          └─────────── HS heading (1-4 digits)
```

### AHTN vs National Tariff

| Level | Digits | Harmonization |
|-------|--------|---------------|
| HS Heading | 4 | Global (WCO) |
| HS Subheading | 6 | Global (WCO) |
| AHTN | 8 | ASEAN regional |
| National | 9-10+ | Country-specific |

### Singapore Tariff Code

Singapore uses 8-digit codes aligned with AHTN:

```
Singapore Code: 8517.13.00
                │      │
                │      └─ AHTN subdivision (typically 00)
                └───────── HS subheading
```

---

## HS Code Updates

### Revision Cycle

The WCO revises the HS every 5-6 years:

| Version | Effective Date | Key Changes |
|---------|----------------|-------------|
| HS 2007 | Jan 2007 | Environmental goods |
| HS 2012 | Jan 2012 | Food security, chemical weapons |
| HS 2017 | Jan 2017 | ITA products, drones |
| HS 2022 | Jan 2022 | E-waste, COVID items, smartphones |
| HS 2027 | Jan 2027 (expected) | TBD |

### HS 2022 Notable Changes

| Product | Old Code | New Code |
|---------|----------|----------|
| Smartphones | 8517.12 | 8517.13 (new) |
| 3D printers | Various | 8485.10/20 (new) |
| Drones/UAVs | 8802.xx | 8806.xx (new chapter) |
| E-waste | Various | 8549.xx (new) |
| COVID test kits | Various | 3822.19/90 |

---

## Singapore-Specific Considerations

### Tariff Classification

Singapore Customs provides classification services:

- **Free classification advice**: Via online form or customs counter
- **Binding ruling**: Formal ruling valid for 3 years
- **AHTN alignment**: Singapore uses 8-digit AHTN codes

### Controlled Goods

Some HS codes trigger permit requirements:

| HS Chapter | Controlled Items | Authority |
|------------|-----------------|-----------|
| 01-05 | Live animals, animal products | AVS |
| 27 | Petroleum products | EMA |
| 28-29 | Chemicals | NEA |
| 36 | Explosives | SPF |
| 84-85 | Strategic goods | Customs |
| 93 | Arms and ammunition | SPF |

### GST and Duties

| HS Code Range | Typical Duty | GST |
|---------------|--------------|-----|
| Most products | 0% | 9% |
| Alcoholic beverages (22.xx) | Excise duty | 9% |
| Tobacco (24.xx) | Excise duty | 9% |
| Motor vehicles (87.xx) | ARF + Excise | 9% |
| Petroleum (27.xx) | Excise duty | 9% |

---

## Best Practices for HS Classification

### Do's

1. **Read section and chapter notes** first
2. **Apply GIR in sequence** (don't jump to Rule 3)
3. **Consider the product at import** (condition when cleared)
4. **Use Explanatory Notes** for guidance
5. **Obtain binding rulings** for complex products
6. **Keep supporting documentation** (specs, brochures)

### Don'ts

1. **Don't rely solely on product name** - classify by characteristics
2. **Don't assume consistency** - different countries may classify differently
3. **Don't ignore packaging** - some products include packaging in code
4. **Don't copy supplier's code blindly** - verify independently
5. **Don't forget updates** - HS codes change periodically

---

## Classification Resources

### Official Sources

| Resource | URL | Use |
|----------|-----|-----|
| WCO HS Database | harmonized-system.org | Official nomenclature |
| Singapore Customs | customs.gov.sg | SG tariff codes |
| ASEAN Tariff Finder | tariff-finder.asean.org | AHTN lookup |
| UN COMTRADE | comtrade.un.org | Trade statistics |

### Tools

| Tool | Description |
|------|-------------|
| **Singapore Tariff Finder** | Official SG customs tool for code lookup |
| **ASEAN Tariff Finder** | Regional tariff rates by HS code |
| **TradeNet** | Singapore's trade declaration system |
| **HS Explanatory Notes** | WCO publication with detailed guidance |

---

## Common Classification Challenges

### Challenge 1: Multi-Function Products

**Example**: Smartwatch with health monitoring

Options:
- 8517.62 (communication device)
- 9102.xx (watch)
- 9018.xx (medical device)

**Solution**: Apply GIR 3(b) - essential character. If primary function is timekeeping with smart features → 9102.12 (smart watches)

### Challenge 2: Kits and Sets

**Example**: First aid kit

Options:
- Classify each item separately
- Classify as retail set under GIR 3(b)

**Solution**: If put up for retail sale and items work together → classify by essential character component

### Challenge 3: Parts vs. Finished Goods

**Example**: Car door (unassembled)

Options:
- 8708.xx (motor vehicle parts)
- 8302.xx (base metal mountings)

**Solution**: Parts identifiable for specific use → parts heading (8708.xx)

---

## Quick Reference Tables

### Common Products and HS Codes

| Product | HS Code | Notes |
|---------|---------|-------|
| Smartphones | 8517.13 | HS 2022 code |
| Laptops | 8471.30 | Portable <10kg |
| Tablets | 8471.30 | Portable data processing |
| Monitors | 8528.52 | Computer monitors |
| Printers | 8443.31 | Inkjet/laser |
| T-shirts (cotton) | 6109.10 | Knitted |
| Jeans | 6203.42 | Men's woven cotton |
| Coffee (roasted) | 0901.21 | Not decaffeinated |
| Electronics parts | 8473.30 | Parts for ADP machines |
| Lithium batteries | 8506.50 | Lithium primary cells |

### Section XVI: Machinery Quick Guide

| Heading | Products |
|---------|----------|
| 84.15 | Air conditioners |
| 84.18 | Refrigerators, freezers |
| 84.43 | Printing machinery |
| 84.71 | Computers, laptops |
| 85.04 | Transformers, power supplies |
| 85.17 | Phones, smartphones |
| 85.23 | Storage media, USB drives |
| 85.28 | Monitors, TVs |
| 85.42 | Integrated circuits |

---

*Source: World Customs Organization (WCO) Harmonized System*
*For official classification, consult Singapore Customs or obtain a binding ruling.*
