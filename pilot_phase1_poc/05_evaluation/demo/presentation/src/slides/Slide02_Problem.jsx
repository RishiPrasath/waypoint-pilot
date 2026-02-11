import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';

const painPoints = [
  { icon: '🔍', text: 'CS agents spend 15–20 min searching across PDFs, portals, and internal docs per query' },
  { icon: '⚠️', text: 'Singapore customs rules change frequently — outdated answers cause compliance issues' },
  { icon: '📦', text: 'Carrier-specific procedures (VGM, SI cutoffs) scattered across multiple sources' },
  { icon: '📋', text: 'No single source of truth for internal policies (SLA, booking procedures, escalation)' },
];

export default function Slide02_Problem({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="The Challenge" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="flex flex-col justify-center h-full max-w-3xl">
        {painPoints.map((p, i) => (
          <motion.div
            key={i}
            className="flex items-start gap-4 mb-6 p-4 rounded-lg bg-slate-800/50 border border-slate-700/50"
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 + i * 0.2, duration: 0.5 }}
          >
            <span className="text-2xl mt-0.5">{p.icon}</span>
            <p className="text-lg text-slate-300">{p.text}</p>
          </motion.div>
        ))}
      </div>
    </SlideLayout>
  );
}
