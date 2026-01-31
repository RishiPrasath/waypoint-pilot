/**
 * Confidence level indicator component.
 * Shows a color-coded badge based on confidence level.
 */
export default function Confidence({ level, reason }) {
  const colorMap = {
    High: 'bg-emerald-100 text-emerald-800',
    Medium: 'bg-amber-100 text-amber-800',
    Low: 'bg-rose-100 text-rose-800',
  };

  const colors = colorMap[level] || colorMap.Low;

  return (
    <div className="flex items-center gap-2">
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${colors}`}
      >
        {level} Confidence
      </span>
      {reason && (
        <span className="text-xs text-slate-500">{reason}</span>
      )}
    </div>
  );
}
