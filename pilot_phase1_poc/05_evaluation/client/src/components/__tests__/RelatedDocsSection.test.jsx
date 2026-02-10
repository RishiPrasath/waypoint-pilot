import { render, screen } from '@testing-library/react';
import RelatedDocsSection from '../RelatedDocsSection';

const mockDocs = [
  { title: 'Export Guide', category: 'regulatory', docId: 'sg_export', url: 'https://customs.gov.sg/export' },
  { title: 'Booking SOP', category: 'internal', docId: 'booking_sop', url: null },
  { title: 'Maersk Schedules', category: 'carrier', docId: 'maersk_sched', url: 'https://maersk.com/schedules' },
  { title: 'Incoterms Guide', category: 'reference', docId: 'incoterms', url: null },
];

describe('RelatedDocsSection', () => {
  test('returns null when docs is empty array', () => {
    const { container } = render(<RelatedDocsSection docs={[]} />);
    expect(container.innerHTML).toBe('');
  });

  test('returns null when docs is undefined', () => {
    const { container } = render(<RelatedDocsSection docs={undefined} />);
    expect(container.innerHTML).toBe('');
  });

  test('renders correct number of doc chips', () => {
    render(<RelatedDocsSection docs={mockDocs} />);
    expect(screen.getByText('Export Guide')).toBeInTheDocument();
    expect(screen.getByText('Booking SOP')).toBeInTheDocument();
    expect(screen.getByText('Maersk Schedules')).toBeInTheDocument();
    expect(screen.getByText('Incoterms Guide')).toBeInTheDocument();
  });

  test('renders link for docs with URL', () => {
    render(<RelatedDocsSection docs={mockDocs} />);
    const links = screen.getAllByRole('link');
    expect(links).toHaveLength(2);
    expect(links[0]).toHaveAttribute('href', 'https://customs.gov.sg/export');
    expect(links[1]).toHaveAttribute('href', 'https://maersk.com/schedules');
  });

  test('renders span (not link) for docs without URL', () => {
    render(<RelatedDocsSection docs={[mockDocs[1]]} />);
    expect(screen.queryAllByRole('link')).toHaveLength(0);
    expect(screen.getByText('Booking SOP')).toBeInTheDocument();
  });

  test('renders section header', () => {
    render(<RelatedDocsSection docs={mockDocs} />);
    expect(screen.getByText('Related Documents')).toBeInTheDocument();
  });

  test('all doc links open in new tab with secure rel', () => {
    render(<RelatedDocsSection docs={mockDocs} />);
    const links = screen.getAllByRole('link');
    links.forEach((link) => {
      expect(link).toHaveAttribute('target', '_blank');
      expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    });
  });

  test('all doc links have valid https href', () => {
    render(<RelatedDocsSection docs={mockDocs} />);
    const links = screen.getAllByRole('link');
    links.forEach((link) => {
      const href = link.getAttribute('href');
      expect(href).toBeTruthy();
      expect(href.startsWith('https://')).toBe(true);
    });
  });

  test('links include external-link icon SVG', () => {
    render(<RelatedDocsSection docs={mockDocs} />);
    const links = screen.getAllByRole('link');
    links.forEach((link) => {
      const svg = link.querySelector('svg');
      expect(svg).not.toBeNull();
    });
  });
});
