/**
 * API-specific type definitions for backend compatibility
 */

// ==================== User & Authentication Types ====================

export interface ApiUser {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string | null;
}

export interface AuthState {
  user: ApiUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// ==================== Exercise Types ====================

export interface ApiExercise {
  id: string;
  type: string;
  prompt: string;
  difficulty: number;
  explanation?: string;
  hints?: string[];
  tags?: string[];
}

export interface ExerciseAnswer {
  exercise_id: string;
  user_answer: string;
  time_taken?: number;
  session_id?: number;
  // Custom exercise metadata
  verb?: string;
  tense?: string;
  person?: string;
  correct_answer?: string;
  alternative_answers?: string[];
  explanation?: string;
  trigger_phrase?: string;
}

export interface AnswerValidation {
  is_correct: boolean;
  correct_answer: string;
  user_answer: string;
  feedback: string;
  explanation?: string;
  score: number;
  alternative_answers?: string[];
  // Enhanced feedback
  error_type?: string;
  suggestions?: string[];
  related_rules?: string[];
  encouragement?: string;
  next_steps?: string[];
  // Spaced repetition
  next_review_date?: string;
  interval_days?: number;
  difficulty_level?: string;
}

export interface ExerciseState {
  currentExercise: ApiExercise | null;
  exerciseHistory: ApiExercise[];
  currentAnswer: string;
  isSubmitting: boolean;
  lastValidation: AnswerValidation | null;
  filters: ExerciseFilters;
  availableTypes: string[];
  isLoading: boolean;
  error: string | null;
}

export interface ExerciseFilters {
  difficulty?: number;
  exercise_type?: string;
  tags?: string[];
  limit: number;
  random_order: boolean;
}

export interface ExerciseListResponse {
  exercises: ApiExercise[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

// ==================== Custom Practice Types ====================

export interface CustomPracticeRequest {
  verbs: string[];
  tense: string;
  persons: string[];
  difficulty: number;
  custom_context: string;
  trigger_category: string;
  exercise_count: number;
  include_hints: boolean;
  include_explanations: boolean;
}

export interface GeneratedExercise {
  id: string;
  verb: string;
  verb_translation: string;
  tense: string;
  person: string;
  prompt: string;
  correct_answer: string;
  alternative_answers: string[];
  hint?: string;
  explanation?: string;
  trigger_phrase?: string;
  difficulty: number;
}

export interface CustomPracticeResponse {
  exercises: GeneratedExercise[];
  total: number;
  config_summary: {
    verbs: string[];
    verb_count: number;
    tense: string;
    persons: string[];
    difficulty: number;
    trigger_category: string;
    has_custom_context: boolean;
  };
}

export interface AvailableVerb {
  infinitive: string;
  translation: string;
  type: string;
  is_irregular: boolean;
  frequency_rank: number;
}

export interface AvailableVerbsResponse {
  verbs: AvailableVerb[];
  total: number;
}

// ==================== Session Management Types ====================

export interface SessionStartRequest {
  session_type?: string;
}

export interface SessionStartResponse {
  session_id: number;
  started_at: string;
}

export interface SessionEndRequest {
  session_id: number;
}

export interface SessionEndResponse {
  session_id: number;
  started_at: string;
  ended_at: string;
  duration_seconds: number;
  total_exercises: number;
  correct_answers: number;
  score_percentage: number;
  session_type: string;
}

// ==================== Spaced Repetition Types ====================

export interface DueReviewItem {
  verb_id: number;
  verb_infinitive: string;
  verb_translation: string;
  tense: string;
  person?: string;
  days_overdue: number;
  difficulty_level: string;
  easiness_factor: number;
  next_review_date: string;
  review_count: number;
  success_rate: number;
}

export interface DueReviewResponse {
  items: DueReviewItem[];
  total_due: number;
  next_review_date?: string;
}

export interface ReviewStatsResponse {
  total_due: number;
  due_by_difficulty: Record<string, number>;
  average_retention: number;
  total_reviewed: number;
  reviews_today: number;
  streak_days: number;
}

// ==================== Progress Types ====================

export interface ApiProgress {
  user_id: string;
  total_exercises: number;
  correct_answers: number;
  incorrect_answers: number;
  accuracy_rate: number;
  current_streak: number;
  best_streak: number;
  last_practice?: string;
  level: number;
  experience_points: number;
}

export interface ApiStatistics {
  user_id: string;
  overall_stats: {
    total_exercises: number;
    correct_answers: number;
    accuracy_rate: number;
    average_score: number;
  };
  by_type: Record<string, TypeStats>;
  by_difficulty: Record<string, DifficultyStats>;
  recent_performance: RecentPerformance[];
  learning_insights: string[];
  practice_calendar: string[];
}

export interface TypeStats {
  total: number;
  correct: number;
  accuracy: number;
}

export interface DifficultyStats {
  total: number;
  correct: number;
  accuracy: number;
}

export interface RecentPerformance {
  exercise_id: string;
  exercise_type: string;
  is_correct: boolean;
  score: number;
  timestamp: string;
}

export interface ProgressState {
  progress: ApiProgress | null;
  statistics: ApiStatistics | null;
  isLoading: boolean;
  error: string | null;
}

// ==================== UI State Types ====================

export interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  modals: {
    [key: string]: boolean;
  };
  toasts: Toast[];
  isOnline: boolean;
}

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}

// ==================== Settings Types ====================

export interface UserSettings {
  notifications: {
    email: boolean;
    push: boolean;
    streakReminders: boolean;
  };
  practice: {
    dailyGoal: number;
    autoAdvance: boolean;
    showHints: boolean;
    showExplanations: boolean;
  };
  accessibility: {
    fontSize: 'small' | 'medium' | 'large';
    highContrast: boolean;
    reduceMotion: boolean;
  };
  language: {
    interface: string;
    practice: string;
  };
}

export interface SettingsState {
  settings: UserSettings;
  isLoading: boolean;
  error: string | null;
}

// ==================== API Error Types ====================

export interface ApiError {
  error: string;
  message: string;
  details?: Record<string, any>;
  path?: string;
  timestamp?: string;
}

// ==================== Root State ====================

export interface RootState {
  auth: AuthState;
  exercise: ExerciseState;
  progress: ProgressState;
  ui: UIState;
  settings: SettingsState;
}
