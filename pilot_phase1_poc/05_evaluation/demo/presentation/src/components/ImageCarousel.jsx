import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function ImageCarousel() {
  const [manifest, setManifest] = useState(null);
  const [current, setCurrent] = useState(0);
  const [showResponse, setShowResponse] = useState(true);
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    fetch('/demo/screenshots/manifest.json')
      .then(r => r.json())
      .then(setManifest)
      .catch(err => console.warn('Failed to load manifest:', err));
  }, []);

  const queries = manifest?.queries || [];
  const total = queries.length;

  const next = useCallback(() => setCurrent(i => (i + 1) % total), [total]);
  const prev = useCallback(() => setCurrent(i => (i - 1 + total) % total), [total]);

  // Auto-advance every 5s
  useEffect(() => {
    if (paused || total === 0) return;
    const timer = setInterval(next, 5000);
    return () => clearInterval(timer);
  }, [paused, total, next]);

  if (!manifest || total === 0) {
    return <div className="text-slate-500 text-center py-8">Loading demos...</div>;
  }

  const q = queries[current];
  const imgFile = showResponse
    ? (q.files.full || q.files.response)
    : q.files.typed;
  const imgSrc = `/demo/screenshots/${imgFile}`;

  const typeBadge = {
    happy: { label: 'Happy Path', cls: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40' },
    oos: { label: 'Out of Scope', cls: 'bg-red-500/20 text-red-400 border-red-500/40' },
    boundary: { label: 'Boundary', cls: 'bg-amber-500/20 text-amber-400 border-amber-500/40' },
  }[q.type] || { label: q.type, cls: 'bg-slate-500/20 text-slate-400 border-slate-500/40' };

  return (
    <div
      className="flex flex-col h-full"
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-sm text-slate-400">Demo {q.demo}/10</span>
          <span className={`text-xs px-2 py-0.5 rounded-full border ${typeBadge.cls}`}>
            {typeBadge.label}
          </span>
          <span className="text-xs text-slate-500">{q.id}</span>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowResponse(false)}
            className={`text-xs px-3 py-1 rounded ${!showResponse ? 'bg-sky-500/20 text-sky-400' : 'text-slate-500'}`}
          >
            Query
          </button>
          <button
            onClick={() => setShowResponse(true)}
            className={`text-xs px-3 py-1 rounded ${showResponse ? 'bg-sky-500/20 text-sky-400' : 'text-slate-500'}`}
          >
            Response
          </button>
        </div>
      </div>

      {/* Query text */}
      <p className="text-sm text-slate-300 mb-3 italic">"{q.query}"</p>

      {/* Image */}
      <div className="flex-1 relative overflow-hidden rounded-lg border border-slate-700 bg-slate-800 min-h-0">
        <AnimatePresence mode="wait">
          <motion.img
            key={`${current}-${showResponse}`}
            src={imgSrc}
            alt={`Demo ${q.demo}`}
            className="w-full h-full object-contain object-top"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          />
        </AnimatePresence>

        {/* Nav arrows */}
        <button
          onClick={prev}
          className="absolute left-2 top-1/2 -translate-y-1/2 bg-slate-900/70 hover:bg-slate-900/90 text-white rounded-full w-8 h-8 flex items-center justify-center"
        >
          ‹
        </button>
        <button
          onClick={next}
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-slate-900/70 hover:bg-slate-900/90 text-white rounded-full w-8 h-8 flex items-center justify-center"
        >
          ›
        </button>
      </div>

      {/* Dots */}
      <div className="flex justify-center gap-1.5 mt-3">
        {queries.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`w-2 h-2 rounded-full transition-colors ${
              i === current ? 'bg-sky-400' : 'bg-slate-600 hover:bg-slate-500'
            }`}
          />
        ))}
      </div>
    </div>
  );
}
