import { motion } from 'framer-motion';
import SlideLayout from '../components/SlideLayout';
import MermaidDiagram from '../components/MermaidDiagram';

const flowchart = `flowchart TD
    A[User Query] --> B[Query Embedding]
    B --> C[ChromaDB Search\ntop-k=5]
    C --> D{Relevant\nChunks?}
    D -->|Yes| E[Context Assembly]
    D -->|No| F[Graceful Decline]
    E --> G[Groq LLM\nLlama 3.1 8B]
    G --> H[Citation Extraction]
    H --> I[4-Section Response Card]
    style I fill:#0ea5e9,color:#fff`;

export default function Slide07_RAGPipeline({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="RAG Pipeline" subtitle="Query to Answer in 1.2 seconds" slideIndex={slideIndex} totalSlides={totalSlides}>
      <div className="flex items-center justify-center h-full">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          className="max-w-lg"
        >
          <MermaidDiagram chart={flowchart} />
        </motion.div>
      </div>
    </SlideLayout>
  );
}
