import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';

const tiers = [
  {
    label: 'P1',
    title: 'Must-Have',
    badge: 'bg-red-500/20 text-red-400 border-red-500/40',
    items: ['Live TMS/WMS integration', 'Multi-turn conversations', 'User authentication', 'Expand KB to 80+ docs', 'Docker deployment'],
  },
  {
    label: 'P2',
    title: 'Should-Have',
    badge: 'bg-amber-500/20 text-amber-400 border-amber-500/40',
    items: ['Rate limiting & throttling', 'Dynamic ingestion pipeline', 'Structured data tables', 'Logging & analytics', 'Confidence recalibration'],
  },
  {
    label: 'P3',
    title: 'Nice-to-Have',
    badge: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40',
    items: ['Citation fuzzy matching', 'LLM failover (multi-model)', 'Embedding model evaluation', 'Multi-language support'],
  },
];

export default function Slide13_Recommendations({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="Phase 2 Recommendations" subtitle="Where We Go Next" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="grid grid-cols-3 gap-6 h-full items-start pt-4">
        {tiers.map((tier, ti) => (
          <motion.div
            key={ti}
            className="p-5 rounded-xl bg-slate-800/50 border border-slate-700/50"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + ti * 0.15, duration: 0.4 }}
          >
            <div className="flex items-center gap-2 mb-4">
              <span className={`px-2 py-0.5 rounded text-xs font-bold border ${tier.badge}`}>{tier.label}</span>
              <span className="text-sm text-slate-300 font-medium">{tier.title}</span>
            </div>
            <ul className="space-y-2">
              {tier.items.map((item, i) => (
                <li key={i} className="text-sm text-slate-400 flex gap-2">
                  <span className="text-slate-600">•</span>{item}
                </li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>
    </SlideLayout>
  );
}
