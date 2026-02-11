import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';

const weeks = [
  { week: 'Week 1', title: 'Ingestion Pipeline', stats: '29 docs · 400 chunks · 87 tests', color: 'sky' },
  { week: 'Week 2', title: 'RAG Pipeline', stats: 'Express API · React UI · 162 tests', color: 'emerald' },
  { week: 'Week 3', title: 'Retrieval Optimization', stats: '92% hit rate · 709 chunks', color: 'amber' },
  { week: 'Week 4', title: 'Evaluation & Docs', stats: '6 targets met · 38 docs · 217 tests', color: 'blue' },
];

export default function Slide11_Timeline({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="4-Week Journey" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="flex items-center justify-center h-full">
        <div className="flex items-start gap-4 w-full max-w-4xl">
          {weeks.map((w, i) => (
            <motion.div
              key={i}
              className="flex-1 text-center"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + i * 0.25, duration: 0.5 }}
            >
              {/* Node */}
              <div className={`w-12 h-12 mx-auto rounded-full bg-${w.color}-500/20 border-2 border-${w.color}-400 flex items-center justify-center text-${w.color}-400 font-bold text-sm mb-4`}>
                {i + 1}
              </div>
              {/* Line between nodes */}
              {i < weeks.length - 1 && (
                <motion.div
                  className="hidden"
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{ delay: 0.5 + i * 0.25, duration: 0.4 }}
                />
              )}
              <p className="text-xs text-slate-500 mb-1">{w.week}</p>
              <p className="text-sm font-semibold text-slate-200 mb-2">{w.title}</p>
              <p className="text-xs text-slate-400">{w.stats}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Connecting line */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-8 w-3/4 max-w-3xl">
        <motion.div
          className="h-0.5 bg-gradient-to-r from-sky-500 via-emerald-500 to-blue-500"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ delay: 0.2, duration: 1.5 }}
          style={{ transformOrigin: 'left' }}
        />
      </div>
    </SlideLayout>
  );
}
