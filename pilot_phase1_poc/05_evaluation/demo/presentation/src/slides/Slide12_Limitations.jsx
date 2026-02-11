import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';

const columns = [
  {
    title: 'By Design (Phase 2)',
    color: 'sky',
    items: ['No live data (TMS/WMS)', 'No multi-turn conversations', 'No user authentication', 'SG-only regulatory scope', 'English-only'],
  },
  {
    title: 'Technical',
    color: 'amber',
    items: ['Single LLM, no fallback', 'No response caching', 'Local-only ChromaDB', 'No rate limiting', 'No logging/analytics'],
  },
  {
    title: 'Knowledge Base',
    color: 'emerald',
    items: ['30 documents (static)', '92% retrieval hit rate', 'Abbreviation sensitivity', 'No structured data tables', 'No dynamic ingestion'],
  },
];

export default function Slide12_Limitations({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="Known Limitations" subtitle="Honest About Boundaries" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="grid grid-cols-3 gap-6 h-full items-start pt-4">
        {columns.map((col, ci) => (
          <motion.div
            key={ci}
            className="p-5 rounded-xl bg-slate-800/50 border border-slate-700/50"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + ci * 0.15, duration: 0.4 }}
          >
            <h3 className={`text-sm font-semibold text-${col.color}-400 mb-3`}>{col.title}</h3>
            <ul className="space-y-2">
              {col.items.map((item, i) => (
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
