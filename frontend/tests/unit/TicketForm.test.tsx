// frontend/tests/unit/TicketForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import TicketForm from '@/app/components/TicketForm';

describe('TicketForm', () => {
  const mockSubmit = jest.fn();

  beforeEach(() => {
    mockSubmit.mockClear();
  });

  it('renders form fields correctly', () => {
    render(<TicketForm onSubmit={mockSubmit} isLoading={false} />);

    // ✅ استخدمي الـ Placeholder الفعلي من الـ Form
    expect(screen.getByPlaceholderText('e.g., Payment failed on checkout')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Describe the issue in detail...')).toBeInTheDocument();
    expect(screen.getByText('Analyze Ticket')).toBeInTheDocument();
  });

  it('submits form with data', () => {
    render(<TicketForm onSubmit={mockSubmit} isLoading={false} />);

    fireEvent.change(screen.getByPlaceholderText('e.g., Payment failed on checkout'), {
      target: { value: 'Test Ticket' },
    });
    fireEvent.change(screen.getByPlaceholderText('Describe the issue in detail...'), {
      target: { value: 'Test description' },
    });
    fireEvent.click(screen.getByText('Analyze Ticket'));

    expect(mockSubmit).toHaveBeenCalledWith({
      title: 'Test Ticket',
      description: 'Test description',
      resolution_time: undefined,
    });
  });

  it('disables inputs when loading', () => {
    render(<TicketForm onSubmit={mockSubmit} isLoading={true} />);

    expect(screen.getByPlaceholderText('e.g., Payment failed on checkout')).toBeDisabled();
    expect(screen.getByPlaceholderText('Describe the issue in detail...')).toBeDisabled();
    expect(screen.getByText('Analyzing...')).toBeInTheDocument();
  });
});