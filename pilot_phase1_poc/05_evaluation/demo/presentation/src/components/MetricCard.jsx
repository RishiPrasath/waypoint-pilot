import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

export default function MetricCard({ label, target, achieved, unit = '%', color = 'emerald', invert = false }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  const colors = {
    emerald: { bar: 'bg-emerald-500', text: 'text-emerald-400', bg: 'bg-emerald-500/10' },
    sky:     { bar: 'bg-sky-500',     text: 'text-sky-400',     bg: 'bg-sky-500/10' },
  };
  const c = colors[color] || colors.emerald;

  // For bar width: normalize achieved vs target
  const barPercent = invert
    ? Math.min(100, ((target - achieved) / target) * 100 + 50)
    : Math.min(100, (achieved / (target || 1)) * 100);

  const displayValue = typeof achieved === 'string' ? achieved : achieved.toLocaleString();

  return (
    <motion.div
      ref={ref}
      className={`rounded-xl p-5 ${c.bg} border border-slate-700/50`}
      initial={{ opacity: 0, y: 20 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.5 }}
    >
      <p className="text-sm text-slate-400 mb-1">{label}</p>
      <div className="flex items-baseline gap-2 mb-2">
        <span className={`text-3xl font-bold ${c.text}`}>
          {isInView ? displayValue : '0'}
        </span>
        <span className="text-lg text-slate-400">{unit}</span>
      </div>
      <p className="text-xs text-slate-500 mb-3">Target: {target}{unit}</p>
      <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
        <motion.div
          className={`h-full ${c.bar} rounded-full`}
          initial={{ width: 0 }}
          animate={isInView ? { width: `${barPercent}%` } : {}}
          transition={{ duration: 1, ease: 'easeOut' }}
        />
      </div>
    </motion.div>
  );
}
