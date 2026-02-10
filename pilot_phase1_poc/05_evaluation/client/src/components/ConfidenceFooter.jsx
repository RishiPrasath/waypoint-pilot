/**
 * Confidence footer — colored badge with confidence level + metadata stats.
 * Left side: colored dot + level badge + reason text.
 * Right side: monospace retrieval stats (chunks retrieved, used, latency).
 * Returns null if confidence is undefined.
 *
 * @param {Object} props
 * @param {import('../types').Confidence} props.confidence - Confidence level and reason
 * @param {import('../types').ResponseMetadata} props.metadata - Pipeline metadata for stats display
 * @returns {JSX.Element|null}
 */

/** Confidence-level-to-style mapping: bg, text, border, dot Tailwind classes per confidence tier. */
const confidenceStyles = {
  High: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-300', dot: 'bg-emerald-500' },
  Medium: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-300', dot: 'bg-amber-500' },
  Low: { bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-300', dot: 'bg-rose-500' },
};

export default function ConfidenceFooter({ confidence, metadata }) {
  if (!confidence) return null;

  const style = confidenceStyles[confidence.level] || confidenceStyles.Medium;

  return (
    <div className="border-t border-slate-100 px-5 py-3 flex items-center justify-between bg-slate-50/50 rounded-b-xl">
      <div className="flex items-center gap-2.5">
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${style.bg} ${style.text} ${style.border}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${style.dot}`} />
          {confidence.level} confidence
        </span>
        {confidence.reason && (
          <span className="text-xs text-slate-400">{confidence.reason}</span>
        )}
      </div>
      {metadata && (
        <div className="text-xs text-slate-400 font-mono">
          {metadata.chunksRetrieved} retrieved &middot; {metadata.chunksUsed} used &middot; {(metadata.latencyMs / 1000).toFixed(1)}s
        </div>
      )}
    </div>
  );
}
