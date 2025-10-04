import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Input } from '@/components/ui/input';

describe('Input Component', () => {
  it('renders input element', () => {
    render(<Input placeholder="Enter text" />);
    expect(screen.getByPlaceholderText(/enter text/i)).toBeInTheDocument();
  });

  it('handles text input', async () => {
    const user = userEvent.setup();
    render(<Input placeholder="Type here" />);

    const input = screen.getByPlaceholderText(/type here/i);
    await user.type(input, 'Hello World');

    expect(input).toHaveValue('Hello World');
  });

  it('handles onChange event', async () => {
    const user = userEvent.setup();
    const handleChange = jest.fn();
    render(<Input onChange={handleChange} placeholder="Input" />);

    const input = screen.getByPlaceholderText(/input/i);
    await user.type(input, 'a');

    expect(handleChange).toHaveBeenCalled();
  });

  it('supports different input types', () => {
    const { rerender } = render(<Input type="text" placeholder="Text" />);
    expect(screen.getByPlaceholderText(/text/i)).toHaveAttribute('type', 'text');

    rerender(<Input type="email" placeholder="Email" />);
    expect(screen.getByPlaceholderText(/email/i)).toHaveAttribute('type', 'email');

    rerender(<Input type="password" placeholder="Password" />);
    expect(screen.getByPlaceholderText(/password/i)).toHaveAttribute('type', 'password');
  });

  it('disables input when disabled prop is true', () => {
    render(<Input disabled placeholder="Disabled" />);
    expect(screen.getByPlaceholderText(/disabled/i)).toBeDisabled();
  });

  it('applies custom className', () => {
    render(<Input className="custom-input" placeholder="Custom" />);
    expect(screen.getByPlaceholderText(/custom/i)).toHaveClass('custom-input');
  });

  it('forwards ref to input element', () => {
    const ref = jest.fn();
    render(<Input ref={ref} placeholder="Ref test" />);
    expect(ref).toHaveBeenCalled();
  });

  it('supports default value', () => {
    render(<Input defaultValue="Default text" />);
    expect(screen.getByDisplayValue('Default text')).toBeInTheDocument();
  });

  it('supports controlled value', () => {
    const { rerender } = render(<Input value="Initial" onChange={() => {}} />);
    expect(screen.getByDisplayValue('Initial')).toBeInTheDocument();

    rerender(<Input value="Updated" onChange={() => {}} />);
    expect(screen.getByDisplayValue('Updated')).toBeInTheDocument();
  });

  it('supports required attribute', () => {
    render(<Input required placeholder="Required" />);
    expect(screen.getByPlaceholderText(/required/i)).toBeRequired();
  });

  it('supports min and max attributes for number input', () => {
    render(<Input type="number" min={0} max={100} placeholder="Number" />);
    const input = screen.getByPlaceholderText(/number/i);
    expect(input).toHaveAttribute('min', '0');
    expect(input).toHaveAttribute('max', '100');
  });

  it('supports pattern attribute', () => {
    render(<Input pattern="[0-9]*" placeholder="Pattern" />);
    expect(screen.getByPlaceholderText(/pattern/i)).toHaveAttribute('pattern', '[0-9]*');
  });

  it('has proper focus styles', () => {
    render(<Input placeholder="Focus test" />);
    const input = screen.getByPlaceholderText(/focus test/i);
    expect(input).toHaveClass('focus-visible:ring-2');
  });
});
