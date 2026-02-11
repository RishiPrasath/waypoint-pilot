import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';

const sections = [
  { num: 1, name: 'Answer', desc: 'Markdown-rendered with headers, lists, bold text', color: 'sky' },
  { num: 2, name: 'Sources', desc: 'Clickable external URLs with organization names', color: 'emerald' },
  { num: 3, name: 'Related Documents', desc: 'Color-coded category chips from knowledge base', color: 'amber' },
  { num: 4, name: 'Confidence Footer', desc: 'Badge + metadata stats (chunks, latency, model)', color: 'blue' },
];

export default function Slide08_ResponseUX({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="Response UX" subtitle="The 4-Section Response Card" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="grid grid-cols-2 gap-8 h-full items-center">
        {/* Screenshot */}
        <motion.div
          className="relative rounded-lg overflow-hidden border border-slate-700 bg-slate-800"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <img
            src="/demo/screenshots/demo_02_response.png"
            alt="Demo 2 — GST rate response"
            className="w-full h-auto"
          />
        </motion.div>

        {/* Section labels */}
        <div className="space-y-4">
          {sections.map((s, i) => (
            <motion.div
              key={i}
              className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/50 border border-slate-700/50"
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + i * 0.15, duration: 0.4 }}
            >
              <span className={`w-7 h-7 rounded-full bg-${s.color}-500/20 text-${s.color}-400 flex items-center justify-center text-sm font-bold shrink-0`}>
                {s.num}
              </span>
              <div>
                <p className="text-slate-200 font-medium">{s.name}</p>
                <p className="text-sm text-slate-400">{s.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </SlideLayout>
  );
}
