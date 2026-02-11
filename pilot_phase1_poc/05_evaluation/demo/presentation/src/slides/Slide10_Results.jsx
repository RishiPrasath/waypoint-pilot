import SlideLayout from '../components/SlideLayout';
import MetricCard from '../components/MetricCard';

const metrics = [
  { label: 'Deflection Rate', target: 40, achieved: 87.2, unit: '%', color: 'emerald' },
  { label: 'Citation Accuracy', target: 80, achieved: 96.0, unit: '%', color: 'sky' },
  { label: 'Hallucination Rate', target: 15, achieved: 2.0, unit: '%', color: 'emerald', invert: true },
  { label: 'OOS Handling', target: 90, achieved: 100.0, unit: '%', color: 'sky' },
  { label: 'Avg Latency', target: 5000, achieved: 1182, unit: 'ms', color: 'emerald', invert: true },
  { label: 'System Stability', target: '', achieved: 'Stable', unit: '', color: 'sky' },
];

export default function Slide10_Results({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="Results Dashboard" subtitle="All 6 Targets Exceeded" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="grid grid-cols-3 gap-5 max-w-4xl mx-auto">
        {metrics.map((m, i) => (
          <MetricCard key={i} {...m} />
        ))}
      </div>
    </SlideLayout>
  );
}
