import { motion } from 'framer-motion';

export default function SlideLayout({ title, subtitle, children, slideIndex, totalSlides }) {
  return (
    <div className="slide-container">
      <div className="flex-1 flex flex-col px-16 py-10 overflow-hidden">
        {title && (
          <div className="mb-8">
            <h1 className="text-4xl font-bold gradient-text">{title}</h1>
            {subtitle && <p className="text-lg text-slate-400 mt-2">{subtitle}</p>}
          </div>
        )}
        <div className="flex-1 overflow-hidden">{children}</div>
      </div>

      {/* Footer */}
      <div className="px-16 pb-4 flex items-center justify-between text-sm text-slate-500">
        <span>Waypoint Co-Pilot — POC Presentation</span>
        <span>{slideIndex + 1} / {totalSlides}</span>
      </div>

      {/* Progress bar */}
      <div className="h-1 bg-slate-800">
        <motion.div
          className="h-full bg-sky-500"
          initial={{ width: 0 }}
          animate={{ width: `${((slideIndex + 1) / totalSlides) * 100}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>
    </div>
  );
}
