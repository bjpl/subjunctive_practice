import { render, screen } from '@testing-library/react';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

describe('Alert Components', () => {
  describe('Alert', () => {
    it('renders alert element', () => {
      render(<Alert data-testid="alert">Alert content</Alert>);
      expect(screen.getByTestId('alert')).toBeInTheDocument();
    });

    it('applies default variant styles', () => {
      render(<Alert data-testid="alert">Content</Alert>);
      expect(screen.getByTestId('alert')).toHaveClass('border');
    });

    it('applies destructive variant styles', () => {
      render(<Alert variant="destructive" data-testid="alert">Error</Alert>);
      expect(screen.getByTestId('alert')).toHaveClass('destructive');
    });

    it('applies custom className', () => {
      render(<Alert className="custom-alert" data-testid="alert">Content</Alert>);
      expect(screen.getByTestId('alert')).toHaveClass('custom-alert');
    });
  });

  describe('AlertTitle', () => {
    it('renders alert title', () => {
      render(<AlertTitle>Alert Title</AlertTitle>);
      expect(screen.getByText('Alert Title')).toBeInTheDocument();
    });

    it('applies title styles', () => {
      render(<AlertTitle data-testid="title">Title</AlertTitle>);
      expect(screen.getByTestId('title')).toHaveClass('font-medium');
    });
  });

  describe('AlertDescription', () => {
    it('renders alert description', () => {
      render(<AlertDescription>Alert description</AlertDescription>);
      expect(screen.getByText('Alert description')).toBeInTheDocument();
    });

    it('applies description styles', () => {
      render(<AlertDescription data-testid="desc">Description</AlertDescription>);
      expect(screen.getByTestId('desc')).toHaveClass('text-sm');
    });
  });

  describe('Complete Alert', () => {
    it('renders a complete alert with title and description', () => {
      render(
        <Alert>
          <AlertTitle>Success</AlertTitle>
          <AlertDescription>Your changes have been saved.</AlertDescription>
        </Alert>
      );

      expect(screen.getByText('Success')).toBeInTheDocument();
      expect(screen.getByText('Your changes have been saved.')).toBeInTheDocument();
    });
  });
});
