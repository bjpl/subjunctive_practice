/**
 * LocalStorage hook with type safety
 */

import { useState, useEffect, useCallback } from 'react';
import { getStorageItem, setStorageItem, removeStorageItem } from '../lib/storage';

export function useLocalStorage<T>(key: string, defaultValue: T) {
  // Initialize state with value from localStorage or default
  const [value, setValue] = useState<T>(() => {
    return getStorageItem<T>(key, defaultValue);
  });

  // Update localStorage when value changes
  useEffect(() => {
    setStorageItem(key, value);
  }, [key, value]);

  // Remove item from localStorage
  const remove = useCallback(() => {
    removeStorageItem(key);
    setValue(defaultValue);
  }, [key, defaultValue]);

  return [value, setValue, remove] as const;
}
