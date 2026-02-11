import { motion } from 'framer-motion';

export default function Slide14_QA() {
  return (
    <div className="slide-container flex items-center justify-center">
      <div className="text-center">
        <motion.h1
          className="text-6xl font-extrabold gradient-text mb-8"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
        >
          Questions?
        </motion.h1>

        <motion.div
          className="flex flex-wrap justify-center gap-3 max-w-2xl mx-auto mb-10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          {['30 documents', '709 chunks', '92% retrieval', '87% deflection', '96% citation accuracy'].map((stat, i) => (
            <span key={i} className="px-3 py-1.5 rounded-full bg-slate-800 text-slate-300 text-sm border border-slate-700/50">
              {stat}
            </span>
          ))}
        </motion.div>

        <motion.p
          className="text-slate-500 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7, duration: 0.5 }}
        >
          Waypoint Co-Pilot — Phase 1 POC — February 2026
        </motion.p>
      </div>
    </div>
  );
}
