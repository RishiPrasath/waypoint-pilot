"""
Test data for E2E test suite.
Contains all test queries organized by category.
"""

# Category A: Happy Path - Factual queries that should return good answers
HAPPY_PATH_QUERIES = [
    {
        "id": "HP-01",
        "query": "What documents are needed for FCL export from Singapore to Jakarta?",
        "expected_keywords": ["invoice", "packing", "bill of lading", "certificate"],
        "description": "Export documentation requirements",
    },
    {
        "id": "HP-02",
        "query": "What is the current GST rate for imports into Singapore?",
        "expected_keywords": ["9%", "gst", "goods and services tax"],
        "description": "Singapore GST rate",
    },
    {
        "id": "HP-03",
        "query": "What's the difference between CIF and CFR Incoterms?",
        "expected_keywords": ["insurance", "cost", "freight", "risk"],
        "description": "Incoterms comparison",
    },
    {
        "id": "HP-04",
        "query": "How do I find the right HS code for my product?",
        "expected_keywords": ["hs code", "classification", "tariff", "customs"],
        "description": "HS code guidance",
    },
    {
        "id": "HP-05",
        "query": "Does my shipment to Thailand qualify for ATIGA rates?",
        "expected_keywords": ["atiga", "form d", "asean", "preferential"],
        "description": "ATIGA qualification",
    },
    {
        "id": "HP-06",
        "query": "What's Maersk's service coverage in Southeast Asia?",
        "expected_keywords": ["maersk", "service", "route", "port"],
        "description": "Carrier service info",
    },
    {
        "id": "HP-07",
        "query": "What permits are needed for food imports to Indonesia?",
        "expected_keywords": ["bpom", "permit", "indonesia", "food"],
        "description": "Indonesia food import permits",
    },
    {
        "id": "HP-08",
        "query": "What is the difference between Form D and Form E?",
        "expected_keywords": ["form d", "form e", "certificate of origin", "asean", "china"],
        "description": "Certificate of Origin types",
    },
    {
        "id": "HP-09",
        "query": "What are the reefer container options available?",
        "expected_keywords": ["reefer", "temperature", "container", "refrigerated"],
        "description": "Reefer container info",
    },
    {
        "id": "HP-10",
        "query": "How does the Major Exporter Scheme work?",
        "expected_keywords": ["mes", "major exporter", "gst", "suspended"],
        "description": "MES explanation",
    },
]

# Category B: Multi-Source - Queries requiring multiple documents
MULTI_SOURCE_QUERIES = [
    {
        "id": "MS-01",
        "query": "Compare FCL vs LCL for shipping to Malaysia",
        "expected_keywords": ["fcl", "lcl", "container", "consolidation"],
        "description": "FCL vs LCL comparison",
    },
    {
        "id": "MS-02",
        "query": "What documents and permits for electronics export to Indonesia?",
        "expected_keywords": ["export", "indonesia", "permit", "document"],
        "description": "Electronics export to Indonesia",
    },
    {
        "id": "MS-03",
        "query": "Explain customs clearance process with GST implications",
        "expected_keywords": ["customs", "clearance", "gst", "import"],
        "description": "Customs clearance with GST",
    },
    {
        "id": "MS-04",
        "query": "What carriers offer temperature-controlled shipping to Vietnam?",
        "expected_keywords": ["temperature", "reefer", "vietnam", "carrier"],
        "description": "Reefer shipping to Vietnam",
    },
    {
        "id": "MS-05",
        "query": "Full process for ATIGA preferential tariff application",
        "expected_keywords": ["atiga", "form d", "certificate", "origin", "process"],
        "description": "ATIGA application process",
    },
]

# Category C: Out-of-Scope - Queries the system should decline
OUT_OF_SCOPE_QUERIES = [
    {
        "id": "OOS-01",
        "query": "What is the stock price of Maersk today?",
        "expected_behavior": "decline",
        "description": "Live stock data request",
    },
    {
        "id": "OOS-02",
        "query": "Book a shipment for me to Jakarta",
        "expected_behavior": "decline",
        "description": "Action/booking request",
    },
    {
        "id": "OOS-03",
        "query": "What's the weather in Singapore?",
        "expected_behavior": "decline",
        "description": "Unrelated query",
    },
    {
        "id": "OOS-04",
        "query": "Track my shipment BL12345",
        "expected_behavior": "decline",
        "description": "Live tracking request",
    },
    {
        "id": "OOS-05",
        "query": "What are your competitor's rates?",
        "expected_behavior": "decline",
        "description": "Competitor info request",
    },
]

# Category D: Edge Cases
EDGE_CASE_QUERIES = [
    {
        "id": "EC-01",
        "query": "",
        "expected_behavior": "error_or_decline",
        "description": "Empty query",
    },
    {
        "id": "EC-02",
        "query": "a",
        "expected_behavior": "error_or_decline",
        "description": "Single character query",
    },
    {
        "id": "EC-03",
        "query": "What are the detailed requirements for shipping hazardous materials including lithium batteries via sea freight from Singapore port to multiple destinations across Southeast Asia including Malaysia, Indonesia, Thailand, Vietnam, and Philippines, considering all the different regulatory frameworks, documentation requirements, carrier restrictions, packaging standards, labeling requirements, and any special permits that might be needed for each destination country? " * 2,
        "expected_behavior": "handle_gracefully",
        "description": "Very long query (500+ chars)",
    },
    {
        "id": "EC-04",
        "query": "什么是GST? €£¥ Какой налог?",
        "expected_behavior": "handle_gracefully",
        "description": "Unicode/multilingual query",
    },
    {
        "id": "EC-05",
        "query": "SELECT * FROM users; DROP TABLE shipments; --",
        "expected_behavior": "handle_gracefully",
        "description": "SQL injection attempt",
    },
]

# Category E: Concurrent - Queries for parallel execution
CONCURRENT_QUERIES = [
    {
        "id": "CONC-01",
        "query": "What is the GST rate in Singapore?",
        "description": "Concurrent test query 1",
    },
    {
        "id": "CONC-02",
        "query": "What documents are needed for export?",
        "description": "Concurrent test query 2",
    },
    {
        "id": "CONC-03",
        "query": "Explain FOB Incoterms",
        "description": "Concurrent test query 3",
    },
]

# Category F: Error Recovery
ERROR_RECOVERY_SCENARIOS = [
    {
        "id": "ER-01",
        "type": "timeout",
        "description": "API timeout handling",
    },
    {
        "id": "ER-02",
        "type": "malformed",
        "description": "Malformed request handling",
    },
]
