"use client";

import { useState, useMemo } from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Play,
  Settings2,
  BookOpen,
  MessageSquare,
  User,
  Gauge,
  Search,
  X,
  Check,
  Sparkles
} from "lucide-react";

// Common Spanish verbs available for practice
const AVAILABLE_VERBS = [
  { infinitive: "hablar", translation: "to speak", type: "regular" },
  { infinitive: "ser", translation: "to be (essence)", type: "irregular" },
  { infinitive: "estar", translation: "to be (state)", type: "irregular" },
  { infinitive: "tener", translation: "to have", type: "irregular" },
  { infinitive: "hacer", translation: "to do/make", type: "irregular" },
  { infinitive: "poder", translation: "to be able to", type: "stem-changing" },
  { infinitive: "ir", translation: "to go", type: "irregular" },
  { infinitive: "ver", translation: "to see", type: "irregular" },
  { infinitive: "dar", translation: "to give", type: "irregular" },
  { infinitive: "saber", translation: "to know (fact)", type: "irregular" },
  { infinitive: "querer", translation: "to want/love", type: "stem-changing" },
  { infinitive: "pensar", translation: "to think", type: "stem-changing" },
  { infinitive: "venir", translation: "to come", type: "irregular" },
  { infinitive: "decir", translation: "to say/tell", type: "irregular" },
  { infinitive: "encontrar", translation: "to find", type: "stem-changing" },
  { infinitive: "pedir", translation: "to ask for", type: "stem-changing" },
  { infinitive: "sentir", translation: "to feel", type: "stem-changing" },
  { infinitive: "dormir", translation: "to sleep", type: "stem-changing" },
  { infinitive: "vivir", translation: "to live", type: "regular" },
  { infinitive: "creer", translation: "to believe", type: "regular" },
  { infinitive: "estudiar", translation: "to study", type: "regular" },
  { infinitive: "trabajar", translation: "to work", type: "regular" },
  { infinitive: "comer", translation: "to eat", type: "regular" },
  { infinitive: "escribir", translation: "to write", type: "regular" },
  { infinitive: "salir", translation: "to leave", type: "irregular" },
  { infinitive: "conocer", translation: "to know (person)", type: "irregular" },
  { infinitive: "seguir", translation: "to follow", type: "stem-changing" },
  { infinitive: "buscar", translation: "to search", type: "regular" },
  { infinitive: "poner", translation: "to put", type: "irregular" },
  { infinitive: "traer", translation: "to bring", type: "irregular" },
];

const TENSES = [
  { value: "present_subjunctive", label: "Present Subjunctive", description: "Espero que hable" },
  { value: "imperfect_subjunctive", label: "Imperfect Subjunctive (-ra)", description: "Quería que hablara" },
];

const PERSONS = [
  { value: "yo", label: "yo", example: "que yo hable" },
  { value: "tú", label: "tú", example: "que tú hables" },
  { value: "él/ella/usted", label: "él/ella/usted", example: "que él hable" },
  { value: "nosotros", label: "nosotros", example: "que nosotros hablemos" },
  { value: "vosotros", label: "vosotros", example: "que vosotros habléis" },
  { value: "ellos/ellas/ustedes", label: "ellos/ustedes", example: "que ellos hablen" },
];

const DIFFICULTIES = [
  { value: 1, label: "Beginner", description: "Common verbs, simple contexts" },
  { value: 2, label: "Intermediate", description: "More verb types, varied contexts" },
  { value: 3, label: "Advanced", description: "Irregular verbs, complex sentences" },
  { value: 4, label: "Expert", description: "All verb types, nuanced contexts" },
];

const TRIGGER_CATEGORIES = [
  { value: "wishes", label: "Wishes (W)", triggers: ["espero que", "ojalá que", "deseo que"] },
  { value: "emotions", label: "Emotions (E)", triggers: ["me alegra que", "siento que", "temo que"] },
  { value: "impersonal", label: "Impersonal (I)", triggers: ["es importante que", "es necesario que"] },
  { value: "requests", label: "Requests (R)", triggers: ["quiero que", "pido que", "sugiero que"] },
  { value: "doubt", label: "Doubt (D)", triggers: ["dudo que", "no creo que", "es posible que"] },
  { value: "ojalá", label: "Ojalá (O)", triggers: ["ojalá", "ojalá que"] },
];

export interface PracticeConfigOptions {
  verbs: string[];
  tense: string;
  persons: string[];
  difficulty: number;
  customContext: string;
  triggerCategory: string;
  exerciseCount: number;
  includeHints: boolean;
  includeExplanations: boolean;
}

interface PracticeConfigProps {
  onStartPractice: (config: PracticeConfigOptions) => void;
  isLoading?: boolean;
}

export function PracticeConfig({ onStartPractice, isLoading = false }: PracticeConfigProps) {
  const [selectedVerbs, setSelectedVerbs] = useState<string[]>([]);
  const [tense, setTense] = useState("present_subjunctive");
  const [selectedPersons, setSelectedPersons] = useState<string[]>(["yo", "tú", "él/ella/usted"]);
  const [difficulty, setDifficulty] = useState(2);
  const [customContext, setCustomContext] = useState("");
  const [triggerCategory, setTriggerCategory] = useState("all");
  const [exerciseCount, setExerciseCount] = useState(10);
  const [includeHints, setIncludeHints] = useState(true);
  const [includeExplanations, setIncludeExplanations] = useState(true);

  const [verbSearchQuery, setVerbSearchQuery] = useState("");
  const [verbPopoverOpen, setVerbPopoverOpen] = useState(false);

  const filteredVerbs = useMemo(() => {
    if (!verbSearchQuery) return AVAILABLE_VERBS;
    const query = verbSearchQuery.toLowerCase();
    return AVAILABLE_VERBS.filter(
      (v) =>
        v.infinitive.toLowerCase().includes(query) ||
        v.translation.toLowerCase().includes(query)
    );
  }, [verbSearchQuery]);

  const toggleVerb = (verb: string) => {
    setSelectedVerbs((prev) =>
      prev.includes(verb) ? prev.filter((v) => v !== verb) : [...prev, verb]
    );
  };

  const togglePerson = (person: string) => {
    setSelectedPersons((prev) =>
      prev.includes(person) ? prev.filter((p) => p !== person) : [...prev, person]
    );
  };

  const handleStartPractice = () => {
    onStartPractice({
      verbs: selectedVerbs.length > 0 ? selectedVerbs : AVAILABLE_VERBS.map(v => v.infinitive),
      tense,
      persons: selectedPersons,
      difficulty,
      customContext,
      triggerCategory,
      exerciseCount,
      includeHints,
      includeExplanations,
    });
  };

  const getVerbTypeColor = (type: string) => {
    switch (type) {
      case "regular": return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "irregular": return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
      case "stem-changing": return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Settings2 className="h-6 w-6" />
          Configure Your Practice Session
        </CardTitle>
        <CardDescription>
          Customize what you want to practice. Select specific verbs, set the context, and choose your difficulty level.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Verb Selection */}
        <div className="space-y-3">
          <Label className="flex items-center gap-2 text-base font-semibold">
            <BookOpen className="h-4 w-4" />
            Select Verbs to Practice
          </Label>
          <p className="text-sm text-muted-foreground">
            Choose specific verbs or leave empty to practice all {AVAILABLE_VERBS.length} verbs
          </p>

          <Popover open={verbPopoverOpen} onOpenChange={setVerbPopoverOpen}>
            <PopoverTrigger asChild>
              <Button variant="outline" className="w-full justify-between">
                {selectedVerbs.length > 0
                  ? `${selectedVerbs.length} verb${selectedVerbs.length > 1 ? "s" : ""} selected`
                  : "Click to select verbs (or leave empty for all)"}
                <Search className="ml-2 h-4 w-4" />
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-96 p-0" align="start">
              <div className="p-3 border-b">
                <Input
                  placeholder="Search verbs..."
                  value={verbSearchQuery}
                  onChange={(e) => setVerbSearchQuery(e.target.value)}
                  className="h-9"
                />
              </div>
              <div className="max-h-64 overflow-y-auto p-2">
                {filteredVerbs.map((verb) => (
                  <div
                    key={verb.infinitive}
                    className={`flex items-center justify-between p-2 rounded cursor-pointer hover:bg-accent ${
                      selectedVerbs.includes(verb.infinitive) ? "bg-accent" : ""
                    }`}
                    onClick={() => toggleVerb(verb.infinitive)}
                  >
                    <div className="flex items-center gap-2">
                      <div className={`w-4 h-4 rounded border flex items-center justify-center ${
                        selectedVerbs.includes(verb.infinitive)
                          ? "bg-primary border-primary text-primary-foreground"
                          : "border-input"
                      }`}>
                        {selectedVerbs.includes(verb.infinitive) && <Check className="h-3 w-3" />}
                      </div>
                      <span className="font-medium">{verb.infinitive}</span>
                      <span className="text-muted-foreground text-sm">({verb.translation})</span>
                    </div>
                    <Badge variant="secondary" className={getVerbTypeColor(verb.type)}>
                      {verb.type}
                    </Badge>
                  </div>
                ))}
              </div>
              {selectedVerbs.length > 0 && (
                <div className="p-2 border-t">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setSelectedVerbs([])}
                    className="w-full"
                  >
                    Clear selection
                  </Button>
                </div>
              )}
            </PopoverContent>
          </Popover>

          {/* Selected verbs badges */}
          {selectedVerbs.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-2">
              {selectedVerbs.map((verb) => (
                <Badge key={verb} variant="secondary" className="flex items-center gap-1">
                  {verb}
                  <X
                    className="h-3 w-3 cursor-pointer hover:text-destructive"
                    onClick={() => toggleVerb(verb)}
                  />
                </Badge>
              ))}
            </div>
          )}
        </div>

        {/* Situation/Theme Context */}
        <div className="space-y-3">
          <Label className="flex items-center gap-2 text-base font-semibold">
            <MessageSquare className="h-4 w-4" />
            Situation / Theme (Optional)
          </Label>
          <p className="text-sm text-muted-foreground">
            Set a thematic context for your practice. Exercises will be generated around this theme.
          </p>
          <Input
            placeholder="e.g., at a restaurant, travel plans, giving advice, job interview..."
            value={customContext}
            onChange={(e) => setCustomContext(e.target.value)}
          />
          {customContext && (
            <p className="text-xs text-green-600 dark:text-green-400 flex items-center gap-1">
              <Sparkles className="h-3 w-3" />
              Exercises will be themed around: &quot;{customContext}&quot;
            </p>
          )}

          {/* Quick theme suggestions */}
          <div className="flex flex-wrap gap-2">
            {["at a restaurant", "travel", "work/career", "health", "relationships", "school"].map((theme) => (
              <Button
                key={theme}
                type="button"
                variant={customContext === theme ? "default" : "outline"}
                size="sm"
                onClick={() => setCustomContext(customContext === theme ? "" : theme)}
              >
                {theme}
              </Button>
            ))}
          </div>
        </div>

        {/* Tense and Trigger Category Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-3">
            <Label className="text-base font-semibold">Subjunctive Tense</Label>
            <Select value={tense} onValueChange={setTense}>
              <SelectTrigger>
                <SelectValue placeholder="Select tense" />
              </SelectTrigger>
              <SelectContent>
                {TENSES.map((t) => (
                  <SelectItem key={t.value} value={t.value}>
                    <div>
                      <div className="font-medium">{t.label}</div>
                      <div className="text-xs text-muted-foreground">{t.description}</div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-3">
            <Label className="text-base font-semibold">Trigger Category (WEIRDO)</Label>
            <Select value={triggerCategory} onValueChange={setTriggerCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Select category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {TRIGGER_CATEGORIES.map((cat) => (
                  <SelectItem key={cat.value} value={cat.value}>
                    <div>
                      <div className="font-medium">{cat.label}</div>
                      <div className="text-xs text-muted-foreground">
                        {cat.triggers.slice(0, 2).join(", ")}...
                      </div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Person Selection */}
        <div className="space-y-3">
          <Label className="flex items-center gap-2 text-base font-semibold">
            <User className="h-4 w-4" />
            Grammatical Persons
          </Label>
          <p className="text-sm text-muted-foreground">
            Select which persons to practice
          </p>
          <div className="flex flex-wrap gap-2">
            {PERSONS.map((person) => (
              <Button
                key={person.value}
                variant={selectedPersons.includes(person.value) ? "default" : "outline"}
                size="sm"
                onClick={() => togglePerson(person.value)}
                className="min-w-[80px]"
              >
                {person.label}
              </Button>
            ))}
          </div>
        </div>

        {/* Difficulty and Exercise Count Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-3">
            <Label className="flex items-center gap-2 text-base font-semibold">
              <Gauge className="h-4 w-4" />
              Difficulty Level
            </Label>
            <Select value={difficulty.toString()} onValueChange={(v) => setDifficulty(parseInt(v))}>
              <SelectTrigger>
                <SelectValue placeholder="Select difficulty" />
              </SelectTrigger>
              <SelectContent>
                {DIFFICULTIES.map((d) => (
                  <SelectItem key={d.value} value={d.value.toString()}>
                    <div>
                      <div className="font-medium">{d.label}</div>
                      <div className="text-xs text-muted-foreground">{d.description}</div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-3">
            <Label className="text-base font-semibold">Number of Exercises</Label>
            <Select value={exerciseCount.toString()} onValueChange={(v) => setExerciseCount(parseInt(v))}>
              <SelectTrigger>
                <SelectValue placeholder="Select count" />
              </SelectTrigger>
              <SelectContent>
                {[5, 10, 15, 20, 25, 30].map((count) => (
                  <SelectItem key={count} value={count.toString()}>
                    {count} exercises
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Options Toggles */}
        <div className="flex flex-wrap gap-4">
          <Button
            variant={includeHints ? "default" : "outline"}
            size="sm"
            onClick={() => setIncludeHints(!includeHints)}
          >
            {includeHints ? "Hints Enabled" : "Hints Disabled"}
          </Button>
          <Button
            variant={includeExplanations ? "default" : "outline"}
            size="sm"
            onClick={() => setIncludeExplanations(!includeExplanations)}
          >
            {includeExplanations ? "Explanations Enabled" : "Explanations Disabled"}
          </Button>
        </div>

        {/* Start Button */}
        <Button
          size="lg"
          className="w-full mt-6"
          onClick={handleStartPractice}
          disabled={isLoading || selectedPersons.length === 0}
        >
          {isLoading ? (
            "Generating exercises..."
          ) : (
            <>
              <Play className="mr-2 h-5 w-5" />
              Start Practice Session
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  );
}

export default PracticeConfig;
