import { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#0ea5e9',
    primaryTextColor: '#f1f5f9',
    primaryBorderColor: '#38bdf8',
    lineColor: '#64748b',
    secondaryColor: '#1e293b',
    tertiaryColor: '#334155',
    fontFamily: 'Inter, system-ui, sans-serif',
    fontSize: '14px',
  },
  flowchart: { curve: 'basis', padding: 20 },
  pie: { textPosition: 0.75 },
});

let counter = 0;

export default function MermaidDiagram({ chart, className = '' }) {
  const containerRef = useRef(null);
  const [svg, setSvg] = useState('');
  const idRef = useRef(`mermaid-${++counter}`);

  useEffect(() => {
    if (!chart) return;
    let cancelled = false;

    (async () => {
      try {
        const { svg: rendered } = await mermaid.render(idRef.current, chart.trim());
        if (!cancelled) setSvg(rendered);
      } catch (err) {
        console.warn('Mermaid render error:', err);
      }
    })();

    return () => { cancelled = true; };
  }, [chart]);

  return (
    <div
      ref={containerRef}
      className={`flex justify-center items-center ${className}`}
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}
