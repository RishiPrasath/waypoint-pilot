import { render, screen } from '@testing-library/react';
import ConfidenceFooter from '../ConfidenceFooter';

const mockMetadata = {
  query: 'What documents for export?',
  chunksRetrieved: 5,
  chunksUsed: 3,
  latencyMs: 1250,
  model: 'llama-3.1-8b-instant',
};

describe('ConfidenceFooter', () => {
  test('returns null when confidence is undefined', () => {
    const { container } = render(<ConfidenceFooter confidence={undefined} metadata={mockMetadata} />);
    expect(container.innerHTML).toBe('');
  });

  test('renders High confidence badge', () => {
    render(<ConfidenceFooter confidence={{ level: 'High', reason: '3 relevant sources' }} />);
    expect(screen.getByText('High confidence')).toBeInTheDocument();
  });

  test('renders Medium confidence badge', () => {
    render(<ConfidenceFooter confidence={{ level: 'Medium', reason: '2 sources found' }} />);
    expect(screen.getByText('Medium confidence')).toBeInTheDocument();
  });

  test('renders Low confidence badge', () => {
    render(<ConfidenceFooter confidence={{ level: 'Low', reason: 'Only 1 source' }} />);
    expect(screen.getByText('Low confidence')).toBeInTheDocument();
  });

  test('displays confidence reason', () => {
    render(<ConfidenceFooter confidence={{ level: 'High', reason: '3 relevant sources with 2 citations' }} />);
    expect(screen.getByText('3 relevant sources with 2 citations')).toBeInTheDocument();
  });

  test('renders metadata stats when provided', () => {
    render(<ConfidenceFooter confidence={{ level: 'High', reason: 'test' }} metadata={mockMetadata} />);
    expect(screen.getByText(/5 retrieved/)).toBeInTheDocument();
    expect(screen.getByText(/3 used/)).toBeInTheDocument();
    expect(screen.getByText(/1\.3s/)).toBeInTheDocument();
  });

  test('omits metadata section when metadata is undefined', () => {
    render(<ConfidenceFooter confidence={{ level: 'High', reason: 'test' }} />);
    expect(screen.queryByText(/retrieved/)).not.toBeInTheDocument();
  });
});
