/**
 * API-specific type definitions for backend compatibility
 */

// ==================== User & Authentication Types ====================

export interface ApiUser {
  user_id: string;
  username: string;
  email: string;
  full_name?: string;
  created_at: string;
  last_login?: string;
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
}

export interface AnswerValidation {
  is_correct: boolean;
  correct_answer: string;
  user_answer: string;
  feedback: string;
  explanation?: string;
  score: number;
  alternative_answers?: string[];
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
