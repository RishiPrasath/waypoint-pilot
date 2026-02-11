import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';

export default function Slide03_Solution({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="The Solution" subtitle="Before & After" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="grid grid-cols-2 gap-8 h-full items-center">
        {/* Before */}
        <motion.div
          className="p-6 rounded-xl bg-slate-800/60 border border-slate-600/50"
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 0.7, x: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h3 className="text-lg font-semibold text-slate-400 mb-4">Before</h3>
          <ul className="space-y-3 text-slate-400">
            <li className="flex gap-2"><span className="text-red-400">✗</span> Scattered PDFs & portals</li>
            <li className="flex gap-2"><span className="text-red-400">✗</span> Manual search (15–20 min)</li>
            <li className="flex gap-2"><span className="text-red-400">✗</span> Inconsistent answers</li>
            <li className="flex gap-2"><span className="text-red-400">✗</span> No source attribution</li>
            <li className="flex gap-2"><span className="text-red-400">✗</span> Compliance risk</li>
          </ul>
        </motion.div>

        {/* After */}
        <motion.div
          className="p-6 rounded-xl bg-sky-500/10 border border-sky-500/30"
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          <h3 className="text-lg font-semibold text-sky-400 mb-4">After — Waypoint Co-Pilot</h3>
          <ul className="space-y-3 text-slate-200">
            <li className="flex gap-2"><span className="text-emerald-400">✓</span> Single query box</li>
            <li className="flex gap-2"><span className="text-emerald-400">✓</span> Instant sourced answers (~1.2s)</li>
            <li className="flex gap-2"><span className="text-emerald-400">✓</span> 4-section response card</li>
            <li className="flex gap-2"><span className="text-emerald-400">✓</span> Clickable source citations</li>
            <li className="flex gap-2"><span className="text-emerald-400">✓</span> Confidence indicator</li>
          </ul>
        </motion.div>
      </div>
    </SlideLayout>
  );
}
