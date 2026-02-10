import { useState } from "react";

// Mock data simulating a real pipeline response
const mockResponses = {
  import_docs: {
    query: "What documents do I need for importing goods into Singapore?",
    answer: `### Required Documents for Importing Goods into Singapore

The following documents are required for all sea/air freight imports into Singapore:

1. **Bill of Lading (B/L)** or **Air Waybill (AWB)** — issued by the carrier
2. **Commercial Invoice** — minimum 3 copies, showing FOB/CIF value
3. **Packing List** — itemized contents with weights and dimensions
4. **Import Permit** — obtained via TradeNet before cargo arrival
5. **Certificate of Origin (CO)** — required for preferential tariff rates (e.g., Form D under ATIGA)

### Additional Documents (Conditional)

Depending on the goods being imported, you may also need:

- **VGM Declaration** — mandatory for all containerized shipments (SOLAS requirement)
- **Dangerous Goods Declaration** — for hazardous materials
- **Halal Certificate** — for food and cosmetics to certain ASEAN markets
- **SNI Certificate** — for goods transiting to Indonesia (130+ product categories)

> **Note:** All import permits must be obtained *before* cargo arrival. Late permits may result in demurrage charges and customs delays.`,
    sources: [
      {
        title: "Singapore Import Procedures",
        org: "Singapore Customs",
        url: "https://www.customs.gov.sg/businesses/importing-goods/import-procedures",
        section: "Documentation Requirements",
      },
      {
        title: "TradeNet Permit Application Guide",
        org: "Singapore Customs",
        url: "https://www.customs.gov.sg/businesses/national-single-window/tradenet",
        section: "Import Permits",
      },
    ],
    relatedDocs: [
      {
        title: "Singapore Import Procedures",
        category: "regulatory",
        docId: "sg_import_procedures",
        url: "https://www.customs.gov.sg/businesses/importing-goods/import-procedures",
      },
      {
        title: "Singapore GST Guide for Imports",
        category: "regulatory",
        docId: "sg_gst_guide",
        url: "https://www.customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst",
      },
      {
        title: "Booking Procedure",
        category: "internal",
        docId: "booking_procedure",
        url: null,
      },
      {
        title: "Indonesia Import Requirements",
        category: "regulatory",
        docId: "indonesia_import_requirements",
        url: "https://www.insw.go.id",
      },
    ],
    confidence: { level: "High", reason: "5 relevant sources with strong matches" },
    metadata: { chunksRetrieved: 5, chunksUsed: 3, latencyMs: 1840 },
  },
  gst_rate: {
    query: "What's the GST rate for imports into Singapore?",
    answer: `### Singapore Import GST

The current GST rate for imported goods into Singapore is **9%**, effective since 1 January 2024.

### How Import GST is Calculated

GST is computed on the **CIF value** (Cost + Insurance + Freight) plus any duties payable:

> **Import GST = 9% × (CIF Value + Duty Payable)**

### GST Relief & Exemptions

- **Free Trade Zones (FTZ)** — GST is suspended while goods remain in FTZ
- **Major Exporter Scheme (MES)** — approved traders can suspend import GST
- **Approved 3PL Scheme** — qualifying logistics providers can defer GST
- **De minimis threshold** — goods valued ≤ SGD 400 imported via air/post are GST-exempt

For GST refund claims, ensure your company is GST-registered with IRAS.`,
    sources: [
      {
        title: "Singapore GST Guide for Imports",
        org: "Singapore Customs",
        url: "https://www.customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst",
        section: "Current Rates",
      },
      {
        title: "IRAS GST Rate Information",
        org: "IRAS",
        url: "https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/basics-of-gst/current-gst-rates",
        section: null,
      },
    ],
    relatedDocs: [
      {
        title: "Singapore GST Guide for Imports",
        category: "regulatory",
        docId: "sg_gst_guide",
        url: "https://www.customs.gov.sg/businesses/valuation-duties-taxes-fees/goods-and-services-tax-gst",
      },
      {
        title: "Singapore Free Trade Zones",
        category: "regulatory",
        docId: "sg_free_trade_zones",
        url: "https://www.customs.gov.sg/businesses/exporting-goods/export-procedures/free-trade-zones",
      },
    ],
    confidence: { level: "High", reason: "3 relevant sources with verified data" },
    metadata: { chunksRetrieved: 4, chunksUsed: 2, latencyMs: 1520 },
  },
  oos_rate: {
    query: "What's the current freight rate to Jakarta?",
    answer: `I don't have access to live freight rates as they vary by route, carrier, container type, and market conditions.

### How to Get a Rate Quote

To obtain current freight rates to Jakarta, please:

- **Contact our sales team** at sales@waypoint.sg
- **Use the booking portal** to request a spot quote
- **Speak with your account manager** for contracted rate information

### What I Can Help With

I can provide information about:
- Carrier service routes to Jakarta (PIL, Maersk, ONE, Evergreen)
- Transit times from Singapore to Tanjung Priok
- Required documentation for Indonesia imports
- Indonesia customs requirements and LARTAS restrictions`,
    sources: [],
    relatedDocs: [
      {
        title: "PIL Service Summary",
        category: "carrier",
        docId: "pil_service_summary",
        url: "https://www.pilship.com",
      },
      {
        title: "Indonesia Import Requirements",
        category: "regulatory",
        docId: "indonesia_import_requirements",
        url: "https://www.insw.go.id",
      },
    ],
    confidence: { level: "Low", reason: "Out-of-scope query — live rates unavailable" },
    metadata: { chunksRetrieved: 0, chunksUsed: 0, latencyMs: 380 },
  },
};

const categoryColors = {
  regulatory: { bg: "bg-blue-50", text: "text-blue-700", border: "border-blue-200", icon: "🏛️" },
  carrier: { bg: "bg-amber-50", text: "text-amber-700", border: "border-amber-200", icon: "🚢" },
  internal: { bg: "bg-slate-50", text: "text-slate-600", border: "border-slate-200", icon: "📋" },
  reference: { bg: "bg-emerald-50", text: "text-emerald-700", border: "border-emerald-200", icon: "📚" },
};

const confidenceStyles = {
  High: { bg: "bg-emerald-50", text: "text-emerald-700", border: "border-emerald-300", dot: "bg-emerald-500" },
  Medium: { bg: "bg-amber-50", text: "text-amber-700", border: "border-amber-300", dot: "bg-amber-500" },
  Low: { bg: "bg-rose-50", text: "text-rose-700", border: "border-rose-300", dot: "bg-rose-500" },
};

function SourcesSection({ sources }) {
  if (!sources || sources.length === 0) return null;
  return (
    <div className="border-t border-slate-200 px-5 py-4">
      <div className="flex items-center gap-2 mb-3">
        <svg className="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
        </svg>
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Sources</h3>
      </div>
      <div className="space-y-2">
        {sources.map((s, i) => (
          <a
            key={i}
            href={s.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-start gap-3 p-2.5 rounded-lg hover:bg-sky-50 transition-colors duration-150"
          >
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-sky-100 flex items-center justify-center mt-0.5">
              <svg className="w-4 h-4 text-sky-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </div>
            <div className="min-w-0">
              <div className="text-sm font-medium text-sky-700 group-hover:text-sky-800 group-hover:underline">
                {s.title}{s.section ? ` › ${s.section}` : ""}
              </div>
              <div className="text-xs text-slate-400 truncate mt-0.5">{s.org} · {s.url.replace("https://www.", "").split("/")[0]}</div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}

function RelatedDocsSection({ docs }) {
  if (!docs || docs.length === 0) return null;
  return (
    <div className="border-t border-slate-200 px-5 py-4">
      <div className="flex items-center gap-2 mb-3">
        <svg className="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Related Documents</h3>
      </div>
      <div className="flex flex-wrap gap-2">
        {docs.map((doc, i) => {
          const cat = categoryColors[doc.category] || categoryColors.reference;
          return (
            <div key={i} className="group relative">
              {doc.url ? (
                <a
                  href={doc.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border ${cat.bg} ${cat.text} ${cat.border} hover:shadow-sm transition-all duration-150`}
                >
                  <span>{cat.icon}</span>
                  <span>{doc.title}</span>
                  <svg className="w-3 h-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </a>
              ) : (
                <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border ${cat.bg} ${cat.text} ${cat.border}`}>
                  <span>{cat.icon}</span>
                  <span>{doc.title}</span>
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ConfidenceFooter({ confidence, metadata }) {
  const style = confidenceStyles[confidence.level] || confidenceStyles.Low;
  return (
    <div className="border-t border-slate-100 px-5 py-3 flex items-center justify-between bg-slate-50/50 rounded-b-xl">
      <div className="flex items-center gap-3">
        <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${style.bg} ${style.text} ${style.border}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${style.dot}`}></span>
          {confidence.level} Confidence
        </div>
        <span className="text-xs text-slate-400">{confidence.reason}</span>
      </div>
      <div className="text-xs text-slate-400 font-mono">
        {metadata.chunksRetrieved} retrieved · {metadata.chunksUsed} used · {(metadata.latencyMs / 1000).toFixed(1)}s
      </div>
    </div>
  );
}

function SimpleMarkdown({ text }) {
  const lines = text.split("\n");
  const elements = [];
  let i = 0;
  let listItems = [];
  let listType = null;
  let blockquote = [];

  const flushList = () => {
    if (listItems.length > 0) {
      if (listType === "ol") {
        elements.push(
          <ol key={`ol-${elements.length}`} className="list-decimal list-outside ml-5 space-y-1.5 my-3">
            {listItems.map((item, idx) => (
              <li key={idx} className="text-sm text-slate-700 leading-relaxed pl-1">
                <InlineFormat text={item} />
              </li>
            ))}
          </ol>
        );
      } else {
        elements.push(
          <ul key={`ul-${elements.length}`} className="list-disc list-outside ml-5 space-y-1.5 my-3">
            {listItems.map((item, idx) => (
              <li key={idx} className="text-sm text-slate-700 leading-relaxed pl-1">
                <InlineFormat text={item} />
              </li>
            ))}
          </ul>
        );
      }
      listItems = [];
      listType = null;
    }
  };

  const flushBlockquote = () => {
    if (blockquote.length > 0) {
      elements.push(
        <blockquote key={`bq-${elements.length}`} className="border-l-3 border-sky-300 bg-sky-50/50 pl-4 pr-3 py-2.5 my-3 rounded-r-lg">
          {blockquote.map((line, idx) => (
            <p key={idx} className="text-sm text-slate-700 leading-relaxed">
              <InlineFormat text={line} />
            </p>
          ))}
        </blockquote>
      );
      blockquote = [];
    }
  };

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed.startsWith("### ")) {
      flushList();
      flushBlockquote();
      elements.push(
        <h3 key={`h3-${i}`} className="text-sm font-bold text-slate-800 mt-5 mb-2 first:mt-0">
          {trimmed.slice(4)}
        </h3>
      );
    } else if (trimmed.startsWith("> ")) {
      flushList();
      blockquote.push(trimmed.slice(2));
    } else if (/^\d+\.\s/.test(trimmed)) {
      flushBlockquote();
      if (listType !== "ol") {
        flushList();
        listType = "ol";
      }
      listItems.push(trimmed.replace(/^\d+\.\s/, ""));
    } else if (trimmed.startsWith("- ")) {
      flushBlockquote();
      if (listType !== "ul") {
        flushList();
        listType = "ul";
      }
      listItems.push(trimmed.slice(2));
    } else if (trimmed === "") {
      flushList();
      flushBlockquote();
    } else {
      flushList();
      flushBlockquote();
      elements.push(
        <p key={`p-${i}`} className="text-sm text-slate-700 leading-relaxed my-2">
          <InlineFormat text={trimmed} />
        </p>
      );
    }
    i++;
  }
  flushList();
  flushBlockquote();
  return <>{elements}</>;
}

function InlineFormat({ text }) {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g);
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith("**") && part.endsWith("**")) {
          return <strong key={i} className="font-semibold text-slate-900">{part.slice(2, -2)}</strong>;
        }
        if (part.startsWith("*") && part.endsWith("*")) {
          return <em key={i} className="italic">{part.slice(1, -1)}</em>;
        }
        if (part.startsWith("`") && part.endsWith("`")) {
          return <code key={i} className="text-xs bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded font-mono">{part.slice(1, -1)}</code>;
        }
        return <span key={i}>{part}</span>;
      })}
    </>
  );
}

function ResponseCard({ data }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Section 1: Answer */}
      <div className="px-5 py-5">
        <SimpleMarkdown text={data.answer} />
      </div>

      {/* Section 2: Sources */}
      <SourcesSection sources={data.sources} />

      {/* Section 3: Related Documents */}
      <RelatedDocsSection docs={data.relatedDocs} />

      {/* Section 4: Confidence Footer */}
      <ConfidenceFooter confidence={data.confidence} metadata={data.metadata} />
    </div>
  );
}

export default function WaypointResponseMockup() {
  const [activeQuery, setActiveQuery] = useState("import_docs");
  const [inputValue, setInputValue] = useState(mockResponses.import_docs.query);
  const [isLoading, setIsLoading] = useState(false);

  const handleQuerySwitch = (key) => {
    setIsLoading(true);
    setActiveQuery(key);
    setInputValue(mockResponses[key].query);
    setTimeout(() => setIsLoading(false), 600);
  };

  const data = mockResponses[activeQuery];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-sky-500 to-blue-600 flex items-center justify-center shadow-sm">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-800 leading-tight">Waypoint Co-Pilot</h1>
            <p className="text-xs text-slate-500">Customer Service Assistant</p>
          </div>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-6 space-y-5">
        {/* Query Switcher */}
        <div className="flex gap-2 flex-wrap">
          <span className="text-xs text-slate-400 self-center mr-1">Try:</span>
          {Object.entries(mockResponses).map(([key, val]) => (
            <button
              key={key}
              onClick={() => handleQuerySwitch(key)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-all duration-150 ${
                activeQuery === key
                  ? "bg-sky-50 border-sky-300 text-sky-700 font-medium shadow-sm"
                  : "bg-white border-slate-200 text-slate-500 hover:border-slate-300 hover:text-slate-700"
              }`}
            >
              {key === "import_docs" && "Import Documents"}
              {key === "gst_rate" && "GST Rate"}
              {key === "oos_rate" && "Out-of-Scope"}
            </button>
          ))}
        </div>

        {/* Search Bar */}
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="w-full px-4 py-3 pr-10 rounded-xl border border-slate-300 bg-white text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-transparent shadow-sm"
              placeholder="Ask about shipping, customs, or carrier information..."
            />
            {inputValue && (
              <button
                onClick={() => setInputValue("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-300 hover:text-slate-500"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
          <button className="px-5 py-3 bg-gradient-to-r from-sky-500 to-blue-600 text-white text-sm font-semibold rounded-xl hover:from-sky-600 hover:to-blue-700 shadow-sm hover:shadow transition-all duration-150">
            Search
          </button>
        </div>

        {/* Response Card */}
        {isLoading ? (
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-8">
            <div className="flex items-center justify-center gap-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
                <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></div>
                <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></div>
              </div>
              <span className="text-sm text-slate-400">Searching knowledge base...</span>
            </div>
          </div>
        ) : (
          <ResponseCard data={data} />
        )}

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-4 px-1">
          <span className="text-xs text-slate-400">Document types:</span>
          {Object.entries(categoryColors).map(([key, val]) => (
            <span key={key} className={`inline-flex items-center gap-1 text-xs ${val.text}`}>
              <span>{val.icon}</span> {key.charAt(0).toUpperCase() + key.slice(1)}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
