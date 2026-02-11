import { useState, useEffect, useCallback } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import slides from './slides';

export default function App() {
  const totalSlides = slides.length;

  // Initialize from URL hash
  const getInitialSlide = () => {
    const hash = window.location.hash;
    const match = hash.match(/^#slide-(\d+)$/);
    if (match) {
      const n = parseInt(match[1], 10) - 1;
      if (n >= 0 && n < totalSlides) return n;
    }
    return 0;
  };

  const [current, setCurrent] = useState(getInitialSlide);
  const [direction, setDirection] = useState(0);
  const [showNav, setShowNav] = useState(false);

  const goTo = useCallback((index, dir) => {
    if (index < 0 || index >= totalSlides) return;
    setDirection(dir || (index > current ? 1 : -1));
    setCurrent(index);
    window.location.hash = `slide-${index + 1}`;
  }, [current, totalSlides]);

  const next = useCallback(() => goTo(current + 1, 1), [current, goTo]);
  const prev = useCallback(() => goTo(current - 1, -1), [current, goTo]);

  // Keyboard navigation
  useEffect(() => {
    const handler = (e) => {
      switch (e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
          e.preventDefault();
          next();
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
          e.preventDefault();
          prev();
          break;
        case 'Home':
          e.preventDefault();
          goTo(0, -1);
          break;
        case 'End':
          e.preventDefault();
          goTo(totalSlides - 1, 1);
          break;
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [next, prev, goTo, totalSlides]);

  // Update hash on popstate
  useEffect(() => {
    const handler = () => {
      const slide = getInitialSlide();
      setCurrent(slide);
    };
    window.addEventListener('hashchange', handler);
    return () => window.removeEventListener('hashchange', handler);
  }, []);

  const SlideComponent = slides[current];

  const variants = {
    enter: (dir) => ({ x: dir > 0 ? 300 : -300, opacity: 0 }),
    center: { x: 0, opacity: 1 },
    exit: (dir) => ({ x: dir > 0 ? -300 : 300, opacity: 0 }),
  };

  return (
    <div
      className="relative w-full h-screen overflow-hidden bg-slate-900"
      onMouseMove={() => setShowNav(true)}
      onMouseLeave={() => setShowNav(false)}
    >
      <AnimatePresence mode="wait" custom={direction}>
        <motion.div
          key={current}
          custom={direction}
          variants={variants}
          initial="enter"
          animate="center"
          exit="exit"
          transition={{ duration: 0.3, ease: 'easeInOut' }}
          className="absolute inset-0"
        >
          <SlideComponent slideIndex={current} totalSlides={totalSlides} />
        </motion.div>
      </AnimatePresence>

      {/* Navigation arrows — appear on hover */}
      {showNav && current > 0 && (
        <button
          onClick={prev}
          className="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-slate-800/70 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition-opacity z-10"
        >
          ‹
        </button>
      )}
      {showNav && current < totalSlides - 1 && (
        <button
          onClick={next}
          className="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-slate-800/70 hover:bg-slate-700 text-slate-300 flex items-center justify-center transition-opacity z-10"
        >
          ›
        </button>
      )}
    </div>
  );
}
