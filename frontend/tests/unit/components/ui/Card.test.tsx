import { render, screen } from '@testing-library/react';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from '@/components/ui/card';

describe('Card Components', () => {
  describe('Card', () => {
    it('renders card element', () => {
      render(<Card data-testid="card">Card content</Card>);
      expect(screen.getByTestId('card')).toBeInTheDocument();
    });

    it('applies card styles', () => {
      render(<Card data-testid="card">Content</Card>);
      const card = screen.getByTestId('card');
      expect(card).toHaveClass('rounded-lg', 'border', 'bg-card');
    });

    it('applies custom className', () => {
      render(<Card className="custom-card" data-testid="card">Content</Card>);
      expect(screen.getByTestId('card')).toHaveClass('custom-card');
    });
  });

  describe('CardHeader', () => {
    it('renders header element', () => {
      render(<CardHeader data-testid="header">Header</CardHeader>);
      expect(screen.getByTestId('header')).toBeInTheDocument();
    });

    it('applies header styles', () => {
      render(<CardHeader data-testid="header">Header</CardHeader>);
      expect(screen.getByTestId('header')).toHaveClass('flex', 'flex-col', 'p-6');
    });
  });

  describe('CardTitle', () => {
    it('renders title as h3', () => {
      render(<CardTitle>Card Title</CardTitle>);
      const title = screen.getByText('Card Title');
      expect(title.tagName).toBe('H3');
    });

    it('applies title styles', () => {
      render(<CardTitle data-testid="title">Title</CardTitle>);
      const title = screen.getByTestId('title');
      expect(title).toHaveClass('text-2xl', 'font-semibold');
    });
  });

  describe('CardDescription', () => {
    it('renders description', () => {
      render(<CardDescription>Card description text</CardDescription>);
      expect(screen.getByText('Card description text')).toBeInTheDocument();
    });

    it('applies description styles', () => {
      render(<CardDescription data-testid="desc">Description</CardDescription>);
      expect(screen.getByTestId('desc')).toHaveClass('text-sm', 'text-muted-foreground');
    });
  });

  describe('CardContent', () => {
    it('renders content', () => {
      render(<CardContent data-testid="content">Main content</CardContent>);
      expect(screen.getByTestId('content')).toBeInTheDocument();
    });

    it('applies content styles', () => {
      render(<CardContent data-testid="content">Content</CardContent>);
      expect(screen.getByTestId('content')).toHaveClass('p-6', 'pt-0');
    });
  });

  describe('CardFooter', () => {
    it('renders footer', () => {
      render(<CardFooter data-testid="footer">Footer</CardFooter>);
      expect(screen.getByTestId('footer')).toBeInTheDocument();
    });

    it('applies footer styles', () => {
      render(<CardFooter data-testid="footer">Footer</CardFooter>);
      expect(screen.getByTestId('footer')).toHaveClass('flex', 'items-center', 'p-6');
    });
  });

  describe('Complete Card', () => {
    it('renders a complete card with all sections', () => {
      render(
        <Card>
          <CardHeader>
            <CardTitle>Test Card</CardTitle>
            <CardDescription>Test description</CardDescription>
          </CardHeader>
          <CardContent>
            <p>Card content here</p>
          </CardContent>
          <CardFooter>
            <button>Action</button>
          </CardFooter>
        </Card>
      );

      expect(screen.getByText('Test Card')).toBeInTheDocument();
      expect(screen.getByText('Test description')).toBeInTheDocument();
      expect(screen.getByText('Card content here')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /action/i })).toBeInTheDocument();
    });

    it('maintains proper hierarchy', () => {
      const { container } = render(
        <Card data-testid="card">
          <CardHeader data-testid="header">
            <CardTitle>Title</CardTitle>
          </CardHeader>
        </Card>
      );

      const card = screen.getByTestId('card');
      const header = screen.getByTestId('header');

      expect(card).toContainElement(header);
    });
  });
});
