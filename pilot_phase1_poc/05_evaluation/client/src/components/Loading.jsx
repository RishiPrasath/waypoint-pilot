/**
 * Loading animation — three bouncing sky-blue dots with staggered delays.
 * Matches the response card styling (rounded-xl border shadow-sm).
 * No delay logic — renders immediately.
 *
 * @returns {JSX.Element}
 */
export default function Loading() {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-8">
      <div className="flex items-center justify-center gap-3">
        <div className="flex gap-1">
          <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-2 h-2 bg-sky-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
        <span className="text-sm text-slate-400">Searching knowledge base...</span>
      </div>
    </div>
  );
}
