import { useState, useEffect } from 'react';

/**
 * Loading spinner component with delayed visibility.
 * Shows spinner after 200ms to avoid flash for fast responses.
 */
export default function Loading() {
  const [showSpinner, setShowSpinner] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setShowSpinner(true), 200);
    return () => clearTimeout(timer);
  }, []);

  if (!showSpinner) {
    return null;
  }

  return (
    <div className="flex items-center justify-center py-8">
      <div className="flex items-center gap-3 text-slate-500">
        <svg
          className="animate-spin h-5 w-5 text-sky-500"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
        <span>Searching knowledge base...</span>
      </div>
    </div>
  );
}
