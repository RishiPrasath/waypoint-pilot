import { render, screen } from '@testing-library/react';
import ResponseCard from '../ResponseCard';

const mockData = {
  answer: 'You need **trade declarations** for exports.',
  sources: [
    { title: 'Export Guide', org: 'Singapore Customs', url: 'https://customs.gov.sg/export', section: 'Documents' },
    { title: 'Import Procedures', org: 'Singapore Customs', url: 'https://customs.gov.sg/import', section: 'Overview' },
  ],
  relatedDocs: [
    { title: 'Export Guide', category: 'regulatory', docId: 'sg_export', url: 'https://customs.gov.sg/export' },
    { title: 'Maersk Service', category: 'carrier', docId: 'maersk_svc', url: 'https://maersk.com/services' },
    { title: 'Booking SOP', category: 'internal', docId: 'booking_sop', url: null },
  ],
  citations: [
    { raw: '[Export Guide]', title: 'Export Guide', matched: true },
  ],
  confidence: { level: 'High', reason: '3 relevant sources' },
  metadata: { query: 'export docs', chunksRetrieved: 3, chunksUsed: 2, latencyMs: 250, model: 'llama-3.1-8b-instant' },
};

describe('ResponseCard', () => {
  test('returns null when data is undefined', () => {
    const { container } = render(<ResponseCard data={undefined} />);
    expect(container.innerHTML).toBe('');
  });

  test('renders answer content', () => {
    render(<ResponseCard data={mockData} />);
    expect(screen.getByText(/trade declarations/)).toBeInTheDocument();
  });

  test('renders all 4 child sections when data is populated', () => {
    render(<ResponseCard data={mockData} />);
    // Answer
    expect(screen.getByText(/trade declarations/)).toBeInTheDocument();
    // Sources
    expect(screen.getByText('Sources')).toBeInTheDocument();
    // Related Documents
    expect(screen.getByText('Related Documents')).toBeInTheDocument();
    // Confidence Footer
    expect(screen.getByText('High confidence')).toBeInTheDocument();
  });

  test('all links in card are accessible with target and rel attributes', () => {
    render(<ResponseCard data={mockData} />);
    const links = screen.getAllByRole('link');
    // 2 source links + 2 related doc links with URLs (Booking SOP has null URL = no link)
    expect(links.length).toBeGreaterThanOrEqual(4);
    links.forEach((link) => {
      const href = link.getAttribute('href');
      expect(href).toBeTruthy();
      expect(href.startsWith('https://')).toBe(true);
      expect(link).toHaveAttribute('target', '_blank');
      expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    });
  });
});
