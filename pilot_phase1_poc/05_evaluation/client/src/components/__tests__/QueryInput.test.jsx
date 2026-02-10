import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import QueryInput from '../QueryInput';

describe('QueryInput', () => {
  test('calls onSubmit with trimmed query on form submit', async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();

    render(<QueryInput onSubmit={onSubmit} loading={false} />);
    const input = screen.getByRole('textbox');
    await user.type(input, '  What is GST?  ');
    await user.click(screen.getByRole('button', { name: 'Search' }));

    expect(onSubmit).toHaveBeenCalledWith('What is GST?');
  });

  test('disables submit button when query is empty', () => {
    render(<QueryInput onSubmit={vi.fn()} loading={false} />);
    const submitBtn = screen.getByRole('button', { name: 'Search' });
    expect(submitBtn).toBeDisabled();
  });

  test('disables input and submit when loading', () => {
    render(<QueryInput onSubmit={vi.fn()} loading={true} />);
    const input = screen.getByRole('textbox');
    expect(input).toBeDisabled();
    const submitBtn = screen.getByRole('button', { name: 'Searching...' });
    expect(submitBtn).toBeDisabled();
  });

  test('clear button resets query text', async () => {
    const user = userEvent.setup();
    render(<QueryInput onSubmit={vi.fn()} loading={false} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'test query');
    expect(input).toHaveValue('test query');

    const clearBtn = screen.getByRole('button', { name: 'Clear input' });
    await user.click(clearBtn);
    expect(input).toHaveValue('');
  });
});
