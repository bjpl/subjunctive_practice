import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';
import { TagFilter } from '@/components/practice/TagFilter';

expect.extend(toHaveNoViolations);

// Mock framer-motion
jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  },
  AnimatePresence: ({ children }: any) => <>{children}</>,
}));

describe('TagFilter Component', () => {
  const mockOnTagsChange = jest.fn();
  const mockAvailableTags = ['beginner', 'intermediate', 'advanced', 'trigger-phrases'];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render with default text when no tags selected', () => {
    render(<TagFilter selectedTags={[]} onTagsChange={mockOnTagsChange} />);

    expect(screen.getByText('Filter by tags')).toBeInTheDocument();
  });

  it('should show selected count when tags are selected', () => {
    render(
      <TagFilter
        selectedTags={['beginner', 'intermediate']}
        onTagsChange={mockOnTagsChange}
      />
    );

    expect(screen.getByText('2 tags selected')).toBeInTheDocument();
  });

  it('should use singular form for single tag', () => {
    render(
      <TagFilter
        selectedTags={['beginner']}
        onTagsChange={mockOnTagsChange}
      />
    );

    expect(screen.getByText('1 tag selected')).toBeInTheDocument();
  });

  it('should open popover when button is clicked', async () => {
    const user = userEvent.setup();
    render(<TagFilter selectedTags={[]} onTagsChange={mockOnTagsChange} />);

    const button = screen.getByRole('combobox');
    await user.click(button);

    await waitFor(() => {
      expect(screen.getByPlaceholderText('Search tags...')).toBeInTheDocument();
    });
  });

  it('should filter tags based on search input', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={[]}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    const searchInput = await screen.findByPlaceholderText('Search tags...');
    await user.type(searchInput, 'beg');

    await waitFor(() => {
      expect(screen.getByText('beginner')).toBeInTheDocument();
      expect(screen.queryByText('intermediate')).not.toBeInTheDocument();
    });
  });

  it('should toggle tag selection when clicked', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={[]}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    const beginnerButton = await screen.findByText('beginner');
    await user.click(beginnerButton);

    expect(mockOnTagsChange).toHaveBeenCalledWith(['beginner']);
  });

  it('should remove tag when already selected', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={['beginner']}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    const beginnerButton = await screen.findByText('beginner');
    await user.click(beginnerButton);

    expect(mockOnTagsChange).toHaveBeenCalledWith([]);
  });

  it('should clear all tags when clear button is clicked', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={['beginner', 'intermediate']}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    const clearButton = await screen.findByText('Clear all filters');
    await user.click(clearButton);

    expect(mockOnTagsChange).toHaveBeenCalledWith([]);
  });

  it('should show clear button only when tags are selected', async () => {
    const user = userEvent.setup();
    const { rerender } = render(
      <TagFilter
        selectedTags={[]}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    await waitFor(() => {
      expect(screen.queryByText('Clear all filters')).not.toBeInTheDocument();
    });

    rerender(
      <TagFilter
        selectedTags={['beginner']}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Clear all filters')).toBeInTheDocument();
    });
  });

  it('should display selected tags as badges', () => {
    render(
      <TagFilter
        selectedTags={['beginner', 'intermediate']}
        onTagsChange={mockOnTagsChange}
      />
    );

    // Tags should be visible outside the popover
    const badges = screen.getAllByText(/beginner|intermediate/);
    expect(badges.length).toBeGreaterThan(0);
  });

  it('should remove tag from badge when X is clicked', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={['beginner']}
        onTagsChange={mockOnTagsChange}
      />
    );

    const removeButton = screen.getByLabelText('Remove beginner filter');
    await user.click(removeButton);

    expect(mockOnTagsChange).toHaveBeenCalledWith([]);
  });

  it('should show "No tags found" when search has no results', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={[]}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    const searchInput = await screen.findByPlaceholderText('Search tags...');
    await user.type(searchInput, 'nonexistent');

    await waitFor(() => {
      expect(screen.getByText('No tags found')).toBeInTheDocument();
    });
  });

  it('should show checkmark for selected tags', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={['beginner']}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    await waitFor(() => {
      const beginnerButton = screen.getByText('beginner').closest('button');
      const checkIcon = beginnerButton?.querySelector('svg');
      expect(checkIcon).toBeInTheDocument();
    });
  });

  it('should apply border styling when tags are selected', () => {
    const { container } = render(
      <TagFilter
        selectedTags={['beginner']}
        onTagsChange={mockOnTagsChange}
      />
    );

    const button = screen.getByRole('combobox');
    expect(button).toHaveClass('border-primary');
  });

  it('should use default tags when availableTags not provided', async () => {
    const user = userEvent.setup();
    render(<TagFilter selectedTags={[]} onTagsChange={mockOnTagsChange} />);

    const button = screen.getByRole('combobox');
    await user.click(button);

    await waitFor(() => {
      expect(screen.getByText('trigger-phrases')).toBeInTheDocument();
      expect(screen.getByText('common-verbs')).toBeInTheDocument();
    });
  });

  it('should handle case-insensitive search', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={[]}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    const searchInput = await screen.findByPlaceholderText('Search tags...');
    await user.type(searchInput, 'BEG');

    await waitFor(() => {
      expect(screen.getByText('beginner')).toBeInTheDocument();
    });
  });

  it('should apply custom className', () => {
    const { container } = render(
      <TagFilter
        selectedTags={[]}
        onTagsChange={mockOnTagsChange}
        className="custom-class"
      />
    );

    expect(container.firstChild).toHaveClass('custom-class');
  });

  it('should not have accessibility violations', async () => {
    const { container } = render(
      <TagFilter selectedTags={[]} onTagsChange={mockOnTagsChange} />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should not have accessibility violations when open', async () => {
    const user = userEvent.setup();
    const { container } = render(
      <TagFilter selectedTags={[]} onTagsChange={mockOnTagsChange} />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    await waitFor(async () => {
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  it('should render filter icon', () => {
    const { container } = render(
      <TagFilter selectedTags={[]} onTagsChange={mockOnTagsChange} />
    );

    const filterIcon = container.querySelector('svg');
    expect(filterIcon).toBeInTheDocument();
  });

  it('should handle multiple tag selections', async () => {
    const user = userEvent.setup();
    render(
      <TagFilter
        selectedTags={['beginner']}
        onTagsChange={mockOnTagsChange}
        availableTags={mockAvailableTags}
      />
    );

    const button = screen.getByRole('combobox');
    await user.click(button);

    const intermediateButton = await screen.findByText('intermediate');
    await user.click(intermediateButton);

    expect(mockOnTagsChange).toHaveBeenCalledWith(['beginner', 'intermediate']);
  });
});
