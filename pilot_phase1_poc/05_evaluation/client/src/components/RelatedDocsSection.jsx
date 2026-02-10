/**
 * Related Documents section — category-tagged document chips.
 * Displays unique documents retrieved during the query with category color coding.
 * Chips with URLs render as links; chips without URLs render as spans.
 * Returns null if docs array is empty or undefined.
 *
 * @param {Object} props
 * @param {import('../types').RelatedDoc[]} props.docs - Array of related document objects
 * @returns {JSX.Element|null}
 */

/** Category-to-style mapping: bg, text, border Tailwind classes and emoji icon per KB category. */
const categoryColors = {
  regulatory: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200', icon: '\u{1F3DB}\u{FE0F}' },
  carrier: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200', icon: '\u{1F6A2}' },
  internal: { bg: 'bg-slate-50', text: 'text-slate-600', border: 'border-slate-200', icon: '\u{1F4CB}' },
  reference: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200', icon: '\u{1F4DA}' },
};

const defaultColors = { bg: 'bg-slate-50', text: 'text-slate-600', border: 'border-slate-200', icon: '\u{1F4C4}' };

export default function RelatedDocsSection({ docs }) {
  if (!docs || docs.length === 0) return null;

  return (
    <div className="border-t border-slate-200 px-5 py-4">
      <div className="flex items-center gap-2 mb-3">
        <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Related Documents</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {docs.map((doc) => {
          const cat = categoryColors[doc.category] || defaultColors;
          const classes = `inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border ${cat.bg} ${cat.text} ${cat.border}`;

          if (doc.url) {
            return (
              <a
                key={doc.docId}
                href={doc.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`${classes} hover:shadow-sm transition-all duration-150`}
              >
                <span>{cat.icon}</span>
                <span>{doc.title}</span>
                <svg className="w-3 h-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            );
          }

          return (
            <span key={doc.docId} className={classes}>
              <span>{cat.icon}</span>
              <span>{doc.title}</span>
            </span>
          );
        })}
      </div>
    </div>
  );
}
