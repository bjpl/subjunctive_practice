import { render, screen } from '@testing-library/react';
import { Label } from '@/components/ui/label';

describe('Label Component', () => {
  it('renders label element', () => {
    render(<Label htmlFor="input">Label text</Label>);
    expect(screen.getByText('Label text')).toBeInTheDocument();
  });

  it('associates with input using htmlFor', () => {
    render(
      <div>
        <Label htmlFor="test-input">Username</Label>
        <input id="test-input" />
      </div>
    );

    const label = screen.getByText('Username');
    expect(label).toHaveAttribute('for', 'test-input');
  });

  it('applies custom className', () => {
    render(<Label className="custom-label">Custom</Label>);
    expect(screen.getByText('Custom')).toHaveClass('custom-label');
  });

  it('forwards ref to label element', () => {
    const ref = jest.fn();
    render(<Label ref={ref}>Ref test</Label>);
    expect(ref).toHaveBeenCalled();
  });
});
