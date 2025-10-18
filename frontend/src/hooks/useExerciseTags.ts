import { useState, useCallback } from "react";

interface UseExerciseTagsReturn {
  selectedTags: string[];
  addTag: (tag: string) => void;
  removeTag: (tag: string) => void;
  toggleTag: (tag: string) => void;
  clearTags: () => void;
  setTags: (tags: string[]) => void;
  hasTag: (tag: string) => boolean;
}

export const useExerciseTags = (
  initialTags: string[] = []
): UseExerciseTagsReturn => {
  const [selectedTags, setSelectedTags] = useState<string[]>(initialTags);

  const addTag = useCallback((tag: string) => {
    setSelectedTags((prev) => {
      if (prev.includes(tag)) return prev;
      return [...prev, tag];
    });
  }, []);

  const removeTag = useCallback((tag: string) => {
    setSelectedTags((prev) => prev.filter((t) => t !== tag));
  }, []);

  const toggleTag = useCallback((tag: string) => {
    setSelectedTags((prev) => {
      if (prev.includes(tag)) {
        return prev.filter((t) => t !== tag);
      }
      return [...prev, tag];
    });
  }, []);

  const clearTags = useCallback(() => {
    setSelectedTags([]);
  }, []);

  const setTags = useCallback((tags: string[]) => {
    setSelectedTags(tags);
  }, []);

  const hasTag = useCallback(
    (tag: string) => {
      return selectedTags.includes(tag);
    },
    [selectedTags]
  );

  return {
    selectedTags,
    addTag,
    removeTag,
    toggleTag,
    clearTags,
    setTags,
    hasTag,
  };
};
