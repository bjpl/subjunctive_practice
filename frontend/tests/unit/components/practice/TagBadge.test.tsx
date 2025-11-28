import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';
import { TagBadge, TagList } from '@/components/practice/TagBadge';

expect.extend(toHaveNoViolations);

// Mock framer-motion to avoid animation issues in tests
jest.mock('framer-motion', () => ({
  motion: {
    span: ({ children, ...props }: any) => <span {...props}>{children}</span>,
  },
}));

describe('TagBadge Component', () => {
  it('should render tag text correctly', () => {
    render(<TagBadge tag="beginner" />);
    expect(screen.getByText('beginner')).toBeInTheDocument();
  });

  it('should apply correct color for known tags', () => {
    const { container } = render(<TagBadge tag="trigger-phrases" />);
    const badge = container.querySelector('span');
    expect(badge).toHaveClass('bg-blue-100', 'text-blue-800');
  });

  it('should apply default color for unknown tags', () => {
    const { container } = render(<TagBadge tag="unknown-tag" />);
    const badge = container.querySelector('span');
    expect(badge).toHaveClass('bg-gray-100', 'text-gray-800');
  });

  it('should handle different size variants', () => {
    const { container, rerender } = render(<TagBadge tag="test" size="sm" />);
    let badge = container.querySelector('span');
    expect(badge).toHaveClass('px-2', 'py-0.5', 'text-xs');

    rerender(<TagBadge tag="test" size="md" />);
    badge = container.querySelector('span');
    expect(badge).toHaveClass('px-2.5', 'py-1', 'text-sm');

    rerender(<TagBadge tag="test" size="lg" />);
    badge = container.querySelector('span');
    expect(badge).toHaveClass('px-3', 'py-1.5', 'text-base');
  });

  it('should handle variant prop correctly', () => {
    const { rerender } = render(<TagBadge tag="test" variant="default" />);
    expect(screen.getByText('test')).toBeInTheDocument();

    rerender(<TagBadge tag="test" variant="outline" />);
    expect(screen.getByText('test')).toBeInTheDocument();

    rerender(<TagBadge tag="test" variant="solid" />);
    expect(screen.getByText('test')).toBeInTheDocument();
  });

  it('should show remove button when removable', () => {
    const mockOnRemove = jest.fn();
    render(<TagBadge tag="test" removable onRemove={mockOnRemove} />);

    const removeButton = screen.getByRole('button', { name: /remove test tag/i });
    expect(removeButton).toBeInTheDocument();
  });

  it('should call onRemove when remove button is clicked', async () => {
    const mockOnRemove = jest.fn();
    const user = userEvent.setup();

    render(<TagBadge tag="test" removable onRemove={mockOnRemove} />);

    const removeButton = screen.getByRole('button', { name: /remove test tag/i });
    await user.click(removeButton);

    expect(mockOnRemove).toHaveBeenCalledTimes(1);
  });

  it('should not show remove button when not removable', () => {
    render(<TagBadge tag="test" removable={false} />);

    const removeButton = screen.queryByRole('button');
    expect(removeButton).not.toBeInTheDocument();
  });

  it('should apply custom className', () => {
    const { container } = render(<TagBadge tag="test" className="custom-class" />);
    const badge = container.querySelector('span');
    expect(badge).toHaveClass('custom-class');
  });

  it('should render tag icon', () => {
    const { container } = render(<TagBadge tag="test" />);
    const icon = container.querySelector('svg');
    expect(icon).toBeInTheDocument();
  });

  it('should handle case-insensitive tag colors', () => {
    const { container } = render(<TagBadge tag="BEGINNER" />);
    const badge = container.querySelector('span');
    expect(badge).toHaveClass('bg-emerald-100', 'text-emerald-800');
  });

  it('should not have accessibility violations', async () => {
    const { container } = render(<TagBadge tag="test" />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should not have accessibility violations when removable', async () => {
    const { container } = render(
      <TagBadge tag="test" removable onRemove={() => {}} />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});

describe('TagList Component', () => {
  const mockTags = ['beginner', 'trigger-phrases', 'common-verbs'];

  it('should render all tags when no maxDisplay set', () => {
    render(<TagList tags={mockTags} />);

    expect(screen.getByText('beginner')).toBeInTheDocument();
    expect(screen.getByText('trigger-phrases')).toBeInTheDocument();
    expect(screen.getByText('common-verbs')).toBeInTheDocument();
  });

  it('should limit displayed tags with maxDisplay', () => {
    render(<TagList tags={mockTags} maxDisplay={2} />);

    expect(screen.getByText('beginner')).toBeInTheDocument();
    expect(screen.getByText('trigger-phrases')).toBeInTheDocument();
    expect(screen.queryByText('common-verbs')).not.toBeInTheDocument();
  });

  it('should show remaining count when tags exceed maxDisplay', () => {
    render(<TagList tags={mockTags} maxDisplay={1} />);

    expect(screen.getByText('+2 more')).toBeInTheDocument();
  });

  it('should not show remaining count when all tags displayed', () => {
    render(<TagList tags={mockTags} maxDisplay={10} />);

    expect(screen.queryByText(/more/i)).not.toBeInTheDocument();
  });

  it('should render null when tags array is empty', () => {
    const { container } = render(<TagList tags={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it('should handle undefined tags gracefully', () => {
    const { container } = render(<TagList tags={undefined as any} />);
    expect(container.firstChild).toBeNull();
  });

  it('should call onRemoveTag when tag is removed', async () => {
    const mockOnRemoveTag = jest.fn();
    const user = userEvent.setup();

    render(<TagList tags={mockTags} removable onRemoveTag={mockOnRemoveTag} />);

    const removeButton = screen.getAllByRole('button')[0];
    await user.click(removeButton);

    expect(mockOnRemoveTag).toHaveBeenCalledWith('beginner');
  });

  it('should pass variant to all tags', () => {
    render(<TagList tags={mockTags} variant="outline" />);

    mockTags.forEach(tag => {
      expect(screen.getByText(tag)).toBeInTheDocument();
    });
  });

  it('should pass size to all tags', () => {
    render(<TagList tags={mockTags} size="lg" />);

    mockTags.forEach(tag => {
      expect(screen.getByText(tag)).toBeInTheDocument();
    });
  });

  it('should apply custom className to container', () => {
    const { container } = render(<TagList tags={mockTags} className="custom-list" />);
    const wrapper = container.firstChild;
    expect(wrapper).toHaveClass('custom-list');
  });

  it('should render removable tags correctly', () => {
    render(<TagList tags={mockTags} removable onRemoveTag={() => {}} />);

    const removeButtons = screen.getAllByRole('button');
    expect(removeButtons).toHaveLength(mockTags.length);
  });

  it('should not have accessibility violations', async () => {
    const { container } = render(<TagList tags={mockTags} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should handle single tag', () => {
    render(<TagList tags={['solo-tag']} />);
    expect(screen.getByText('solo-tag')).toBeInTheDocument();
  });

  it('should maintain tag order', () => {
    const orderedTags = ['first', 'second', 'third'];
    const { container } = render(<TagList tags={orderedTags} />);

    const tagElements = container.querySelectorAll('span');
    expect(tagElements[0]).toHaveTextContent('first');
    expect(tagElements[1]).toHaveTextContent('second');
    expect(tagElements[2]).toHaveTextContent('third');
  });

  it('should calculate remaining count correctly', () => {
    const manyTags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5'];
    render(<TagList tags={manyTags} maxDisplay={2} />);

    expect(screen.getByText('+3 more')).toBeInTheDocument();
  });
});
