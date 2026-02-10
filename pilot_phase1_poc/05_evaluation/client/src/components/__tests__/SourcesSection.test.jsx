import { render, screen } from '@testing-library/react';
import SourcesSection from '../SourcesSection';

const mockSources = [
  { title: 'Export Guide', org: 'Singapore Customs', url: 'https://customs.gov.sg/export', section: 'Documents' },
  { title: 'Trade Procedures', org: 'Singapore Customs', url: 'https://www.customs.gov.sg/trade', section: null },
];

describe('SourcesSection', () => {
  test('returns null when sources is empty array', () => {
    const { container } = render(<SourcesSection sources={[]} />);
    expect(container.innerHTML).toBe('');
  });

  test('returns null when sources is undefined', () => {
    const { container } = render(<SourcesSection sources={undefined} />);
    expect(container.innerHTML).toBe('');
  });

  test('renders correct number of source links', () => {
    render(<SourcesSection sources={mockSources} />);
    const links = screen.getAllByRole('link');
    expect(links).toHaveLength(2);
    expect(links[0]).toHaveAttribute('href', 'https://customs.gov.sg/export');
    expect(links[0]).toHaveAttribute('target', '_blank');
  });

  test('displays title with section when provided', () => {
    render(<SourcesSection sources={mockSources} />);
    expect(screen.getByText(/Export Guide — Documents/)).toBeInTheDocument();
  });

  test('displays title without section separator when section is null', () => {
    render(<SourcesSection sources={mockSources} />);
    expect(screen.getByText('Trade Procedures')).toBeInTheDocument();
  });

  test('extracts domain from URL correctly', () => {
    render(<SourcesSection sources={mockSources} />);
    // Both URLs have customs.gov.sg domain — verify both are rendered
    const domainElements = screen.getAllByText(/customs\.gov\.sg/);
    expect(domainElements).toHaveLength(2);
  });

  test('renders section header', () => {
    render(<SourcesSection sources={mockSources} />);
    expect(screen.getByText('Sources')).toBeInTheDocument();
  });

  test('all source links open in new tab with secure rel', () => {
    render(<SourcesSection sources={mockSources} />);
    const links = screen.getAllByRole('link');
    links.forEach((link) => {
      expect(link).toHaveAttribute('target', '_blank');
      expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    });
  });

  test('all source links have valid https href', () => {
    render(<SourcesSection sources={mockSources} />);
    const links = screen.getAllByRole('link');
    links.forEach((link) => {
      const href = link.getAttribute('href');
      expect(href).toBeTruthy();
      expect(href.startsWith('https://')).toBe(true);
    });
  });
});
