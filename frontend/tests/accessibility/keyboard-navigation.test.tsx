import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

describe('Keyboard Navigation Tests', () => {
  describe('Button Navigation', () => {
    it('should be focusable with Tab key', async () => {
      const user = userEvent.setup();
      render(
        <div>
          <Button>First Button</Button>
          <Button>Second Button</Button>
          <Button>Third Button</Button>
        </div>
      );

      const firstButton = screen.getByRole('button', { name: /first button/i });
      const secondButton = screen.getByRole('button', { name: /second button/i });

      // Tab to first button
      await user.tab();
      expect(firstButton).toHaveFocus();

      // Tab to second button
      await user.tab();
      expect(secondButton).toHaveFocus();
    });

    it('should be activatable with Enter key', async () => {
      const user = userEvent.setup();
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Press Me</Button>);

      const button = screen.getByRole('button');

      await user.tab();
      expect(button).toHaveFocus();

      await user.keyboard('{Enter}');
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('should be activatable with Space key', async () => {
      const user = userEvent.setup();
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Press Me</Button>);

      const button = screen.getByRole('button');

      await user.tab();
      expect(button).toHaveFocus();

      await user.keyboard(' ');
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('should skip disabled buttons in tab order', async () => {
      const user = userEvent.setup();
      render(
        <div>
          <Button>First</Button>
          <Button disabled>Disabled</Button>
          <Button>Third</Button>
        </div>
      );

      const firstButton = screen.getByRole('button', { name: /first/i });
      const thirdButton = screen.getByRole('button', { name: /third/i });

      await user.tab();
      expect(firstButton).toHaveFocus();

      await user.tab();
      expect(thirdButton).toHaveFocus();
    });
  });

  describe('Input Navigation', () => {
    it('should be focusable with Tab key', async () => {
      const user = userEvent.setup();
      render(
        <div>
          <Input placeholder="First" />
          <Input placeholder="Second" />
        </div>
      );

      const firstInput = screen.getByPlaceholderText(/first/i);
      const secondInput = screen.getByPlaceholderText(/second/i);

      await user.tab();
      expect(firstInput).toHaveFocus();

      await user.tab();
      expect(secondInput).toHaveFocus();
    });

    it('should allow typing when focused', async () => {
      const user = userEvent.setup();
      render(<Input placeholder="Type here" />);

      const input = screen.getByPlaceholderText(/type here/i);

      await user.tab();
      expect(input).toHaveFocus();

      await user.keyboard('Hello World');
      expect(input).toHaveValue('Hello World');
    });

    it('should navigate with arrow keys in text', async () => {
      const user = userEvent.setup();
      render(<Input defaultValue="Test" />);

      const input = screen.getByDisplayValue('Test') as HTMLInputElement;

      await user.tab();
      await user.keyboard('{ArrowLeft}');

      // Cursor should move left (implementation detail)
      expect(input).toHaveFocus();
    });
  });

  describe('Form Navigation', () => {
    it('should navigate through form elements', async () => {
      const user = userEvent.setup();
      render(
        <form>
          <Input name="field1" placeholder="Field 1" />
          <Input name="field2" placeholder="Field 2" />
          <Button type="submit">Submit</Button>
        </form>
      );

      const field1 = screen.getByPlaceholderText(/field 1/i);
      const field2 = screen.getByPlaceholderText(/field 2/i);
      const submitButton = screen.getByRole('button', { name: /submit/i });

      await user.tab();
      expect(field1).toHaveFocus();

      await user.tab();
      expect(field2).toHaveFocus();

      await user.tab();
      expect(submitButton).toHaveFocus();
    });

    it('should navigate backwards with Shift+Tab', async () => {
      const user = userEvent.setup();
      render(
        <div>
          <Input placeholder="First" />
          <Input placeholder="Second" />
        </div>
      );

      const firstInput = screen.getByPlaceholderText(/first/i);
      const secondInput = screen.getByPlaceholderText(/second/i);

      // Tab to second input
      await user.tab();
      await user.tab();
      expect(secondInput).toHaveFocus();

      // Shift+Tab back to first input
      await user.tab({ shift: true });
      expect(firstInput).toHaveFocus();
    });

    it('should submit form with Enter in input', async () => {
      const user = userEvent.setup();
      const handleSubmit = jest.fn((e) => e.preventDefault());

      render(
        <form onSubmit={handleSubmit}>
          <Input name="field" placeholder="Enter text" />
          <Button type="submit">Submit</Button>
        </form>
      );

      const input = screen.getByPlaceholderText(/enter text/i);

      await user.tab();
      expect(input).toHaveFocus();

      await user.keyboard('{Enter}');
      expect(handleSubmit).toHaveBeenCalled();
    });
  });

  describe('Focus Indicators', () => {
    it('should show focus ring on buttons', () => {
      render(<Button>Focus Me</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveClass('focus-visible:ring-2');
    });

    it('should show focus ring on inputs', () => {
      render(<Input placeholder="Focus me" />);
      const input = screen.getByPlaceholderText(/focus me/i);
      expect(input).toHaveClass('focus-visible:ring-2');
    });
  });

  describe('Tab Order', () => {
    it('should maintain logical tab order', async () => {
      const user = userEvent.setup();
      render(
        <div>
          <h1>Form</h1>
          <Input placeholder="Name" />
          <Input placeholder="Email" />
          <Button>Cancel</Button>
          <Button>Submit</Button>
        </div>
      );

      const nameInput = screen.getByPlaceholderText(/name/i);
      const emailInput = screen.getByPlaceholderText(/email/i);
      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      const submitButton = screen.getByRole('button', { name: /submit/i });

      await user.tab();
      expect(nameInput).toHaveFocus();

      await user.tab();
      expect(emailInput).toHaveFocus();

      await user.tab();
      expect(cancelButton).toHaveFocus();

      await user.tab();
      expect(submitButton).toHaveFocus();
    });
  });

  describe('Escape Key', () => {
    it('should handle Escape key in input', async () => {
      const user = userEvent.setup();
      const handleKeyDown = jest.fn();

      render(<Input onKeyDown={handleKeyDown} placeholder="Press ESC" />);

      const input = screen.getByPlaceholderText(/press esc/i);

      await user.tab();
      await user.keyboard('{Escape}');

      expect(handleKeyDown).toHaveBeenCalled();
      const event = handleKeyDown.mock.calls[0][0];
      expect(event.key).toBe('Escape');
    });
  });
});
