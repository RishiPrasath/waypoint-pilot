/**
 * Citations list component.
 * Displays source citations with links.
 */
export default function Citations({ citations }) {
  // Filter to only show matched citations
  const matchedCitations = citations?.filter(c => c.matched) || [];

  if (matchedCitations.length === 0) {
    return null;
  }

  return (
    <div className="mt-4 pt-4 border-t border-slate-200">
      <h3 className="text-sm font-medium text-slate-700 mb-2">Sources</h3>
      <ul className="space-y-1">
        {matchedCitations.map((citation, index) => {
          const url = citation.sourceUrls?.[0];
          const displayTitle = citation.fullTitle || citation.title;
          const section = citation.section ? ` > ${citation.section}` : '';

          return (
            <li key={index} className="text-sm">
              {url ? (
                <a
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sky-600 hover:text-sky-800 hover:underline inline-flex items-center gap-1"
                >
                  <svg
                    className="w-3.5 h-3.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                    />
                  </svg>
                  {displayTitle}{section}
                </a>
              ) : (
                <span className="text-slate-600 inline-flex items-center gap-2">
                  <svg
                    className="w-3.5 h-3.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  {displayTitle}{section}
                  <span className="text-xs bg-slate-100 px-1.5 py-0.5 rounded">
                    Internal
                  </span>
                </span>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
