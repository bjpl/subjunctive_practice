import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

expect.extend(toHaveNoViolations);

describe('Accessibility Tests - UI Components', () => {
  describe('Button Component', () => {
    it('should not have accessibility violations', async () => {
      const { container } = render(<Button>Click me</Button>);
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should have accessible name', () => {
      const { getByRole } = render(<Button>Submit Form</Button>);
      expect(getByRole('button', { name: /submit form/i })).toBeInTheDocument();
    });

    it('should support aria-label', async () => {
      const { container } = render(<Button aria-label="Close dialog">X</Button>);
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should have proper disabled state', async () => {
      const { container, getByRole } = render(<Button disabled>Disabled</Button>);
      expect(getByRole('button')).toBeDisabled();
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  describe('Input Component', () => {
    it('should not have accessibility violations when labeled', async () => {
      const { container } = render(
        <div>
          <Label htmlFor="test-input">Username</Label>
          <Input id="test-input" />
        </div>
      );
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should support aria-label when no visible label', async () => {
      const { container } = render(<Input aria-label="Search" placeholder="Search..." />);
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should support aria-describedby for error messages', async () => {
      const { container } = render(
        <div>
          <Label htmlFor="email">Email</Label>
          <Input id="email" aria-describedby="email-error" aria-invalid="true" />
          <span id="email-error">Invalid email address</span>
        </div>
      );
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should have proper required state', async () => {
      const { container, getByLabelText } = render(
        <div>
          <Label htmlFor="required-input">Required Field *</Label>
          <Input id="required-input" required aria-required="true" />
        </div>
      );
      expect(getByLabelText(/required field/i)).toHaveAttribute('required');
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  describe('Card Component', () => {
    it('should not have accessibility violations', async () => {
      const { container } = render(
        <Card>
          <CardHeader>
            <CardTitle>Card Title</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Card content goes here</p>
          </CardContent>
        </Card>
      );
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should have proper heading hierarchy', async () => {
      const { container, getByRole } = render(
        <Card>
          <CardHeader>
            <CardTitle>Main Heading</CardTitle>
          </CardHeader>
        </Card>
      );
      expect(getByRole('heading', { level: 3 })).toBeInTheDocument();
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  describe('Alert Component', () => {
    it('should not have accessibility violations', async () => {
      const { container } = render(
        <Alert>
          <AlertTitle>Success</AlertTitle>
          <AlertDescription>Your changes have been saved.</AlertDescription>
        </Alert>
      );
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    it('should have proper role for different variants', async () => {
      const { container: defaultContainer } = render(
        <Alert>
          <AlertDescription>Info message</AlertDescription>
        </Alert>
      );
      let results = await axe(defaultContainer);
      expect(results).toHaveNoViolations();

      const { container: destructiveContainer } = render(
        <Alert variant="destructive">
          <AlertDescription>Error message</AlertDescription>
        </Alert>
      );
      results = await axe(destructiveContainer);
      expect(results).toHaveNoViolations();
    });
  });

  describe('Label Component', () => {
    it('should properly associate with input', async () => {
      const { container, getByLabelText } = render(
        <div>
          <Label htmlFor="test">Test Label</Label>
          <Input id="test" />
        </div>
      );
      expect(getByLabelText('Test Label')).toBeInTheDocument();
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  describe('Form Accessibility', () => {
    it('should have accessible form with validation', async () => {
      const { container } = render(
        <form>
          <div>
            <Label htmlFor="username">Username *</Label>
            <Input
              id="username"
              name="username"
              required
              aria-required="true"
              aria-describedby="username-error"
            />
            <span id="username-error" role="alert" aria-live="polite">
              Username is required
            </span>
          </div>
          <div>
            <Label htmlFor="email">Email *</Label>
            <Input
              id="email"
              name="email"
              type="email"
              required
              aria-required="true"
            />
          </div>
          <Button type="submit">Submit</Button>
        </form>
      );
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });
});
