/**
 * 4-section response card assembling Answer, Sources, Related Documents, and Confidence Footer.
 * Uses react-markdown with remark-gfm for answer rendering with custom Tailwind component mapping.
 * Returns null if data is undefined.
 *
 * @param {Object} props
 * @param {import('../types').QueryResponse} props.data - Full API response object
 * @returns {JSX.Element|null}
 */
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import SourcesSection from './SourcesSection';
import RelatedDocsSection from './RelatedDocsSection';
import ConfidenceFooter from './ConfidenceFooter';

/** Custom react-markdown component mapping with Tailwind classes matching the UX mockup. */
const markdownComponents = {
  h3: ({ children }) => (
    <h3 className="text-sm font-bold text-slate-800 mt-5 mb-2 first:mt-0">{children}</h3>
  ),
  p: ({ children }) => (
    <p className="text-sm text-slate-700 leading-relaxed my-2">{children}</p>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal list-outside ml-5 space-y-1.5 my-3">{children}</ol>
  ),
  ul: ({ children }) => (
    <ul className="list-disc list-outside ml-5 space-y-1.5 my-3">{children}</ul>
  ),
  li: ({ children }) => (
    <li className="text-sm text-slate-700 leading-relaxed pl-1">{children}</li>
  ),
  strong: ({ children }) => (
    <strong className="font-semibold text-slate-900">{children}</strong>
  ),
  em: ({ children }) => (
    <em className="italic">{children}</em>
  ),
  blockquote: ({ children }) => (
    <blockquote className="border-l-3 border-sky-300 bg-sky-50/50 pl-4 pr-3 py-2.5 my-3 rounded-r-lg">{children}</blockquote>
  ),
  code: ({ children }) => (
    <code className="text-xs bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded font-mono">{children}</code>
  ),
};

export default function ResponseCard({ data }) {
  if (!data) return null;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Section 1: Answer */}
      <div className="px-5 py-5">
        <Markdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
          {data.answer}
        </Markdown>
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
