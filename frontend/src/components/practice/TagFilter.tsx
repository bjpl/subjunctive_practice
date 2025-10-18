"use client";

import * as React from "react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { Check, ChevronDown, X, Tag, Filter } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { motion, AnimatePresence } from "framer-motion";

const COMMON_TAGS = [
  "trigger-phrases",
  "common-verbs",
  "beginner",
  "intermediate",
  "advanced",
  "a1-level",
  "a2-level",
  "b1-level",
  "b2-level",
  "subjunctive-present",
  "subjunctive-imperfect",
  "irregular-verbs",
  "regular-verbs",
  "doubt-uncertainty",
  "emotion-feelings",
  "wish-desire",
];

interface TagFilterProps {
  selectedTags: string[];
  onTagsChange: (tags: string[]) => void;
  availableTags?: string[];
  className?: string;
}

export const TagFilter: React.FC<TagFilterProps> = ({
  selectedTags,
  onTagsChange,
  availableTags = COMMON_TAGS,
  className,
}) => {
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredTags = availableTags.filter((tag) =>
    tag.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleTag = (tag: string) => {
    if (selectedTags.includes(tag)) {
      onTagsChange(selectedTags.filter((t) => t !== tag));
    } else {
      onTagsChange([...selectedTags, tag]);
    }
  };

  const clearAllTags = () => {
    onTagsChange([]);
  };

  return (
    <div className={cn("flex items-center gap-2", className)}>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className={cn(
              "justify-between min-w-[200px]",
              selectedTags.length > 0 && "border-primary"
            )}
          >
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4" />
              <span>
                {selectedTags.length > 0
                  ? `${selectedTags.length} tag${selectedTags.length > 1 ? "s" : ""} selected`
                  : "Filter by tags"}
              </span>
            </div>
            <ChevronDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[300px] p-0" align="start">
          <div className="flex flex-col">
            {/* Search Input */}
            <div className="p-2 border-b">
              <input
                type="text"
                placeholder="Search tags..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>

            {/* Tag List */}
            <div className="max-h-[300px] overflow-y-auto p-2">
              {filteredTags.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  No tags found
                </p>
              ) : (
                <div className="space-y-1">
                  {filteredTags.map((tag) => {
                    const isSelected = selectedTags.includes(tag);
                    return (
                      <button
                        key={tag}
                        onClick={() => toggleTag(tag)}
                        className={cn(
                          "w-full flex items-center gap-2 px-3 py-2 text-sm rounded-md transition-colors",
                          "hover:bg-accent hover:text-accent-foreground",
                          isSelected && "bg-accent"
                        )}
                      >
                        <div
                          className={cn(
                            "flex h-4 w-4 items-center justify-center rounded-sm border",
                            isSelected
                              ? "bg-primary border-primary text-primary-foreground"
                              : "border-muted-foreground"
                          )}
                        >
                          {isSelected && <Check className="h-3 w-3" />}
                        </div>
                        <Tag className="h-3 w-3" />
                        <span className="flex-1 text-left">{tag}</span>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Footer Actions */}
            {selectedTags.length > 0 && (
              <>
                <Separator />
                <div className="p-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={clearAllTags}
                    className="w-full justify-center"
                  >
                    Clear all filters
                  </Button>
                </div>
              </>
            )}
          </div>
        </PopoverContent>
      </Popover>

      {/* Active Tags Display */}
      <AnimatePresence>
        {selectedTags.length > 0 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="flex flex-wrap gap-1.5"
          >
            {selectedTags.map((tag) => (
              <Badge
                key={tag}
                variant="secondary"
                className="gap-1 pr-1"
              >
                {tag}
                <button
                  onClick={() => toggleTag(tag)}
                  className="ml-1 rounded-full hover:bg-muted-foreground/20 p-0.5"
                  aria-label={`Remove ${tag} filter`}
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
