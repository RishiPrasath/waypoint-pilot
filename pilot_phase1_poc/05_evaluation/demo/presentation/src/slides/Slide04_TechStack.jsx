import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';

const cols = [
  {
    title: 'Data Layer',
    color: 'emerald',
    items: ['ChromaDB 0.5.23', 'all-MiniLM-L6-v2 (ONNX)', 'Python 3.11+'],
  },
  {
    title: 'API Layer',
    color: 'sky',
    items: ['Express / Node.js 18', 'REST API', 'Groq LLM Client'],
  },
  {
    title: 'UI Layer',
    color: 'blue',
    items: ['React 18', 'Tailwind CSS', 'Markdown Renderer'],
  },
];

const highlights = [
  'Fully local except LLM',
  'No PyTorch / CUDA required',
  '$0 infrastructure cost',
];

export default function Slide04_TechStack({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="Tech Stack" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="flex flex-col h-full justify-center">
        {/* LLM top bar */}
        <motion.div
          className="mb-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-center"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="text-amber-400 font-semibold">LLM — Groq API (Llama 3.1 8B Instant)</span>
        </motion.div>

        {/* Three columns */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          {cols.map((col, ci) => (
            <motion.div
              key={ci}
              className="p-5 rounded-xl bg-slate-800/60 border border-slate-700/50"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + ci * 0.15, duration: 0.5 }}
            >
              <h3 className={`text-sm font-semibold mb-3 text-${col.color}-400`}>{col.title}</h3>
              <ul className="space-y-2">
                {col.items.map((item, i) => (
                  <li key={i} className="text-slate-300 text-sm">{item}</li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Highlights */}
        <motion.div
          className="flex gap-6 justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.5 }}
        >
          {highlights.map((h, i) => (
            <span key={i} className="px-4 py-2 rounded-full bg-slate-800 text-slate-300 text-sm border border-slate-700/50">
              {h}
            </span>
          ))}
        </motion.div>
      </div>
    </SlideLayout>
  );
}
