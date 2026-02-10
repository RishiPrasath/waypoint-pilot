/**
 * Sources section — clickable external URLs with org + domain subtitle.
 * Renders a list of source links extracted from matched citations.
 * Returns null if sources array is empty or undefined.
 *
 * @param {Object} props
 * @param {import('../types').Source[]} props.sources - Array of source objects with title, org, url, section
 * @returns {JSX.Element|null}
 */
export default function SourcesSection({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="border-t border-slate-200 px-5 py-4">
      <div className="flex items-center gap-2 mb-3">
        <svg className="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
        </svg>
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Sources</span>
      </div>
      <div className="space-y-1">
        {sources.map((source, i) => {
          const domain = source.url.replace('https://www.', '').replace('https://', '').split('/')[0];
          return (
            <a
              key={`${source.url}-${i}`}
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-start gap-3 p-2.5 rounded-lg hover:bg-sky-50 transition-colors duration-150"
            >
              <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-sky-100 flex items-center justify-center">
                <svg className="w-4 h-4 text-sky-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </div>
              <div className="min-w-0 flex-1">
                <div className="text-sm font-medium text-sky-700 group-hover:text-sky-800 group-hover:underline">
                  {source.title}{source.section ? ` — ${source.section}` : ''}
                </div>
                <div className="text-xs text-slate-400 truncate mt-0.5">
                  {source.org ? `${source.org} · ` : ''}{domain}
                </div>
              </div>
            </a>
          );
        })}
      </div>
    </div>
  );
}
