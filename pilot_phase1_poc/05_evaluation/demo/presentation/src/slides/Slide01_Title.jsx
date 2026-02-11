import { motion } from 'framer-motion';

export default function Slide01_Title() {
  return (
    <div className="slide-container flex items-center justify-center">
      <div className="text-center">
        <motion.h1
          className="text-7xl font-extrabold gradient-text mb-6"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          Waypoint Co-Pilot
        </motion.h1>

        <motion.p
          className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          RAG-Based Customer Service Assistant for Freight Forwarding
        </motion.p>

        <motion.div
          className="flex items-center justify-center gap-4 mb-10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7, duration: 0.6 }}
        >
          <span className="px-4 py-2 rounded-full bg-sky-500/20 text-sky-400 border border-sky-500/40 text-sm font-medium">
            Phase 1 POC — Complete
          </span>
          <span className="px-4 py-2 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 text-sm font-medium">
            All 6 Evaluation Targets Met
          </span>
        </motion.div>

        <motion.p
          className="text-slate-500"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.6 }}
        >
          February 2026
        </motion.p>
      </div>
    </div>
  );
}
