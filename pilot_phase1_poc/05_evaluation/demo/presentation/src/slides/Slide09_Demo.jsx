import SlideLayout from '../components/SlideLayout';
import ImageCarousel from '../components/ImageCarousel';

export default function Slide09_Demo({ slideIndex, totalSlides }) {
  return (
    <SlideLayout title="Live Demo Gallery" subtitle="10 Queries Across Happy Path, Boundary & Out-of-Scope" slideIndex={slideIndex} totalSlides={totalSlides}>
      <ImageCarousel />
    </SlideLayout>
  );
}
