import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';
import MermaidDiagram from '../components/MermaidDiagram';

const categories = [
  { name: 'Regulatory', count: 14, desc: 'SG Customs, ASEAN trade, import/export', color: 'sky' },
  { name: 'Carrier', count: 6, desc: 'Maersk, PIL, ONE, SIA Cargo, Hapag-Lloyd, Evergreen', color: 'emerald' },
  { name: 'Reference', count: 3, desc: 'Incoterms 2020, HS Codes, Container Specs', color: 'amber' },
  { name: 'Internal', count: 7, desc: 'SLA, Booking Procedure, Escalation, FAQ', color: 'blue' },
];

const pieChart = `pie title Knowledge Base Composition
    "Regulatory (14)" : 14
    "Carrier (6)" : 6
    "Reference (3)" : 3
    "Internal (7)" : 7`;

export default function Slide05_KnowledgeBase({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="Knowledge Base" subtitle="30 Documents · 709 Chunks · 4 Categories" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="grid grid-cols-2 gap-8 h-full items-center">
        {/* Categories */}
        <div className="space-y-4">
          {categories.map((cat, i) => (
            <motion.div
              key={i}
              className="flex items-center gap-4 p-3 rounded-lg bg-slate-800/50 border border-slate-700/50"
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 + i * 0.15, duration: 0.4 }}
            >
              <span className={`text-2xl font-bold text-${cat.color}-400 w-10 text-right`}>{cat.count}</span>
              <div>
                <p className="text-slate-200 font-medium">{cat.name}</p>
                <p className="text-sm text-slate-400">{cat.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Mermaid pie */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          <MermaidDiagram chart={pieChart} />
        </motion.div>
      </div>
    </SlideLayout>
  );
}
