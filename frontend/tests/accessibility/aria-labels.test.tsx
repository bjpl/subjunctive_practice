import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

describe('ARIA Labels and Roles Tests', () => {
  describe('Button ARIA', () => {
    it('should have accessible name from text content', () => {
      render(<Button>Save Changes</Button>);
      expect(screen.getByRole('button', { name: /save changes/i })).toBeInTheDocument();
    });

    it('should have accessible name from aria-label', () => {
      render(<Button aria-label="Close dialog">×</Button>);
      expect(screen.getByRole('button', { name: /close dialog/i })).toBeInTheDocument();
    });

    it('should have accessible name from aria-labelledby', () => {
      render(
        <div>
          <span id="delete-label">Delete Item</span>
          <Button aria-labelledby="delete-label">
            <svg>
              <title>Trash icon</title>
            </svg>
          </Button>
        </div>
      );
      expect(screen.getByRole('button', { name: /delete item/i })).toBeInTheDocument();
    });

    it('should indicate pressed state with aria-pressed', () => {
      render(<Button aria-pressed="true">Toggle On</Button>);
      const button = screen.getByRole('button', { name: /toggle on/i });
      expect(button).toHaveAttribute('aria-pressed', 'true');
    });

    it('should indicate expanded state with aria-expanded', () => {
      render(<Button aria-expanded="true">Expand Menu</Button>);
      const button = screen.getByRole('button', { name: /expand menu/i });
      expect(button).toHaveAttribute('aria-expanded', 'true');
    });
  });

  describe('Input ARIA', () => {
    it('should have accessible name from associated label', () => {
      render(
        <div>
          <Label htmlFor="username">Username</Label>
          <Input id="username" />
        </div>
      );
      expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    });

    it('should have accessible name from aria-label', () => {
      render(<Input aria-label="Search products" placeholder="Search..." />);
      expect(screen.getByLabelText(/search products/i)).toBeInTheDocument();
    });

    it('should indicate required fields with aria-required', () => {
      render(
        <div>
          <Label htmlFor="email">Email</Label>
          <Input id="email" required aria-required="true" />
        </div>
      );
      const input = screen.getByLabelText(/email/i);
      expect(input).toHaveAttribute('aria-required', 'true');
      expect(input).toBeRequired();
    });

    it('should indicate invalid state with aria-invalid', () => {
      render(
        <div>
          <Label htmlFor="email">Email</Label>
          <Input id="email" aria-invalid="true" />
        </div>
      );
      const input = screen.getByLabelText(/email/i);
      expect(input).toHaveAttribute('aria-invalid', 'true');
    });

    it('should describe errors with aria-describedby', () => {
      render(
        <div>
          <Label htmlFor="password">Password</Label>
          <Input id="password" aria-describedby="password-error" aria-invalid="true" />
          <span id="password-error">Password must be at least 8 characters</span>
        </div>
      );
      const input = screen.getByLabelText(/password/i);
      expect(input).toHaveAttribute('aria-describedby', 'password-error');
      expect(screen.getByText(/password must be at least 8 characters/i)).toBeInTheDocument();
    });

    it('should indicate disabled state', () => {
      render(
        <div>
          <Label htmlFor="disabled-input">Disabled Field</Label>
          <Input id="disabled-input" disabled />
        </div>
      );
      const input = screen.getByLabelText(/disabled field/i);
      expect(input).toBeDisabled();
    });
  });

  describe('Form Field Groups', () => {
    it('should group related inputs with fieldset and legend', () => {
      const { container } = render(
        <fieldset>
          <legend>Contact Information</legend>
          <div>
            <Label htmlFor="name">Name</Label>
            <Input id="name" />
          </div>
          <div>
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" />
          </div>
        </fieldset>
      );

      const fieldset = container.querySelector('fieldset');
      const legend = screen.getByText(/contact information/i);

      expect(fieldset).toContainElement(legend);
      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    });
  });

  describe('Alert Messages', () => {
    it('should use role="alert" for important messages', () => {
      render(
        <div role="alert" aria-live="assertive">
          Error: Failed to save changes
        </div>
      );
      expect(screen.getByRole('alert')).toHaveTextContent(/error.*failed to save/i);
    });

    it('should use aria-live for dynamic content', () => {
      render(
        <div aria-live="polite" aria-atomic="true">
          3 new messages
        </div>
      );
      const liveRegion = screen.getByText(/3 new messages/i);
      expect(liveRegion).toHaveAttribute('aria-live', 'polite');
      expect(liveRegion).toHaveAttribute('aria-atomic', 'true');
    });
  });

  describe('Loading States', () => {
    it('should indicate loading with aria-busy', () => {
      render(
        <div aria-busy="true" aria-label="Loading content">
          <span>Loading...</span>
        </div>
      );
      const loadingDiv = screen.getByLabelText(/loading content/i);
      expect(loadingDiv).toHaveAttribute('aria-busy', 'true');
    });

    it('should use aria-live for loading announcements', () => {
      render(
        <div role="status" aria-live="polite">
          <span>Loading exercises...</span>
        </div>
      );
      expect(screen.getByRole('status')).toHaveTextContent(/loading exercises/i);
    });
  });

  describe('Navigation Landmarks', () => {
    it('should have proper navigation role', () => {
      render(
        <nav aria-label="Main navigation">
          <ul>
            <li>
              <a href="/dashboard">Dashboard</a>
            </li>
            <li>
              <a href="/practice">Practice</a>
            </li>
          </ul>
        </nav>
      );
      expect(screen.getByRole('navigation', { name: /main navigation/i })).toBeInTheDocument();
    });

    it('should have proper main role', () => {
      render(
        <main>
          <h1>Dashboard</h1>
          <p>Welcome to your dashboard</p>
        </main>
      );
      expect(screen.getByRole('main')).toBeInTheDocument();
    });
  });

  describe('Interactive Elements', () => {
    it('should have proper button role and name for icon buttons', () => {
      render(
        <button type="button" aria-label="Settings">
          <svg aria-hidden="true">
            <path d="..." />
          </svg>
        </button>
      );
      expect(screen.getByRole('button', { name: /settings/i })).toBeInTheDocument();
    });

    it('should hide decorative images from screen readers', () => {
      const { container } = render(
        <div>
          <img src="logo.png" alt="" aria-hidden="true" />
          <img src="profile.png" alt="User profile picture" />
        </div>
      );

      const decorativeImg = container.querySelector('img[aria-hidden="true"]');
      const informativeImg = screen.getByAltText(/user profile picture/i);

      expect(decorativeImg).toBeInTheDocument();
      expect(informativeImg).toBeInTheDocument();
    });
  });

  describe('Autocomplete', () => {
    it('should use autocomplete attribute for common fields', () => {
      render(
        <div>
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" autoComplete="email" />
        </div>
      );
      const input = screen.getByLabelText(/email/i);
      expect(input).toHaveAttribute('autocomplete', 'email');
    });

    it('should use autocomplete for password fields', () => {
      render(
        <div>
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" autoComplete="current-password" />
        </div>
      );
      const input = screen.getByLabelText(/password/i);
      expect(input).toHaveAttribute('autocomplete', 'current-password');
    });
  });
});
