import Markdown from 'react-markdown';
import Citations from './Citations';
import Confidence from './Confidence';

/**
 * Response display component.
 * Shows the answer with markdown formatting, citations, and confidence.
 */
export default function Response({ data, error }) {
  // Error state
  if (error) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-lg p-4">
        <div className="flex items-center gap-2 text-rose-800">
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <span className="font-medium">Unable to process query</span>
        </div>
        <p className="mt-2 text-sm text-rose-700">{error}</p>
      </div>
    );
  }

  // Empty state
  if (!data) {
    return (
      <div className="text-center py-12 text-slate-500">
        <svg
          className="w-12 h-12 mx-auto mb-4 text-slate-300"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <p>Ask a question to get started</p>
        <p className="text-sm mt-1">
          Try asking about shipping, customs, or carrier information
        </p>
      </div>
    );
  }

  const { answer, citations, confidence, metadata } = data;

  return (
    <div className="space-y-4">
      {/* Answer */}
      <div className="prose prose-slate prose-sm max-w-none">
        <Markdown>{answer}</Markdown>
      </div>

      {/* Citations */}
      <Citations citations={citations} />

      {/* Footer: Confidence + Stats */}
      <div className="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-slate-200">
        <Confidence
          level={confidence?.level}
          reason={confidence?.reason}
        />
        
        {metadata && (
          <div className="text-xs text-slate-400">
            {metadata.chunksRetrieved} chunks retrieved, {metadata.chunksUsed} used
            {metadata.latency?.totalMs && (
              <span> &bull; {(metadata.latency.totalMs / 1000).toFixed(1)}s</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
