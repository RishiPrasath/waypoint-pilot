import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';
import MermaidDiagram from '../components/MermaidDiagram';

const flowchart = `flowchart LR
    A[30 Markdown\nDocuments] --> B[Frontmatter\nExtraction]
    B --> C[Text Chunking\n600 chars / 90 overlap]
    C --> D[Embedding\nall-MiniLM-L6-v2]
    D --> E[ChromaDB\n709 chunks]
    style E fill:#0ea5e9,color:#fff`;

const details = [
  { label: 'Chunk Size', value: '600 chars' },
  { label: 'Overlap', value: '90 chars (15%)' },
  { label: 'Metadata Fields', value: '12 per chunk' },
  { label: 'Embedding Dim', value: '384-d (ONNX)' },
];

export default function Slide06_DataPipeline({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="Data Pipeline" subtitle="From Documents to Vectors" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="flex flex-col h-full justify-center">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <MermaidDiagram chart={flowchart} />
        </motion.div>

        <motion.div
          className="flex gap-6 justify-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
        >
          {details.map((d, i) => (
            <div key={i} className="text-center px-4 py-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
              <p className="text-xs text-slate-500 mb-1">{d.label}</p>
              <p className="text-sm text-sky-400 font-medium">{d.value}</p>
            </div>
          ))}
        </motion.div>
      </div>
    </SlideLayout>
  );
}
