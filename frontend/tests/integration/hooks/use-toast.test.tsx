import { renderHook, act } from '@testing-library/react';
import { useToast } from '@/hooks/use-toast';

describe('useToast Hook', () => {
  it('initializes with empty toast list', () => {
    const { result } = renderHook(() => useToast());
    expect(result.current.toasts).toEqual([]);
  });

  it('can show a toast', () => {
    const { result } = renderHook(() => useToast());

    act(() => {
      result.current.toast({
        title: 'Test Toast',
        description: 'This is a test',
      });
    });

    expect(result.current.toasts).toHaveLength(1);
    expect(result.current.toasts[0].title).toBe('Test Toast');
    expect(result.current.toasts[0].description).toBe('This is a test');
  });

  it('can dismiss a toast', async () => {
    const { result } = renderHook(() => useToast());

    let toastId: string;

    act(() => {
      const { id } = result.current.toast({
        title: 'Test Toast',
      });
      toastId = id!;
    });

    expect(result.current.toasts).toHaveLength(1);

    act(() => {
      result.current.dismiss(toastId!);
    });

    // Toast is marked as not open, but removal is delayed
    expect(result.current.toasts[0]?.open).toBe(false);

    // Wait for removal delay
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 150));
    });

    expect(result.current.toasts).toHaveLength(0);
  });

  it('generates unique IDs for toasts', () => {
    const { result } = renderHook(() => useToast());

    let id1: string;
    let id2: string;

    act(() => {
      const { id } = result.current.toast({ title: 'Toast 1' });
      id1 = id!;
    });

    act(() => {
      const { id } = result.current.toast({ title: 'Toast 2' });
      id2 = id!;
    });

    expect(id1).not.toBe(id2);
    expect(result.current.toasts).toHaveLength(2);
  });

  it('supports different toast variants', () => {
    const { result } = renderHook(() => useToast());

    act(() => {
      result.current.toast({
        title: 'Success',
        variant: 'default',
      });
    });

    act(() => {
      result.current.toast({
        title: 'Error',
        variant: 'destructive',
      });
    });

    expect(result.current.toasts).toHaveLength(2);
    expect(result.current.toasts[0].variant).toBe('default');
    expect(result.current.toasts[1].variant).toBe('destructive');
  });
});
