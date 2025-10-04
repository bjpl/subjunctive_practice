// User types
export interface User {
  id: string;
  username: string;
  email?: string;
  created_at?: string;
  updated_at?: string;
}

// Authentication types
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterCredentials extends LoginCredentials {
  email?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Exercise types
export interface Exercise {
  id: string;
  sentence: string;
  options: string[];
  correct_answer: string;
  explanation?: string;
  difficulty?: "easy" | "medium" | "hard";
  category?: string;
}

export interface ExerciseAttempt {
  exercise_id: string;
  user_answer: string;
  is_correct: boolean;
  attempted_at: string;
}

// Progress types
export interface Progress {
  user_id: string;
  total_exercises: number;
  completed_exercises: number;
  correct_answers: number;
  accuracy: number;
  streak: number;
  last_practice: string;
}

export interface Statistics {
  total_time_spent: number;
  exercises_by_difficulty: {
    easy: number;
    medium: number;
    hard: number;
  };
  exercises_by_category: Record<string, number>;
  daily_progress: Array<{
    date: string;
    exercises_completed: number;
    accuracy: number;
  }>;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface ApiError {
  message: string;
  status: number;
  errors?: Record<string, string[]>;
}

// Form types
export interface LoginFormData {
  username: string;
  password: string;
}

export interface RegisterFormData extends LoginFormData {
  email?: string;
  confirmPassword: string;
}

// Session types
export interface PracticeSession {
  id: string;
  user_id: string;
  started_at: string;
  ended_at?: string;
  exercises_completed: number;
  correct_answers: number;
  total_time: number;
}

// Analytics types
export interface DailyActivity {
  date: string;
  count: number;
  accuracy: number;
}

export interface PerformanceTrend {
  date: string;
  accuracy: number;
  exerciseCount: number;
  averageTime: number;
}

export interface WeakArea {
  category: string;
  accuracy: number;
  totalAttempts: number;
  correctAttempts: number;
  difficulty?: string;
}

export interface LearningInsight {
  type: "weak_area" | "strong_area" | "streak" | "improvement" | "recommendation";
  title: string;
  description: string;
  data?: any;
  priority: "low" | "medium" | "high";
}

// Gamification types
export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: "streak" | "accuracy" | "volume" | "mastery" | "special";
  tier: "bronze" | "silver" | "gold" | "platinum";
  unlocked: boolean;
  unlockedAt?: string;
  progress: number; // 0-100
  requirement: number;
  currentValue: number;
}

export interface LevelInfo {
  currentLevel: number;
  currentXP: number;
  xpForNextLevel: number;
  totalXP: number;
  progressToNextLevel: number; // 0-100
}

export interface Badge {
  id: string;
  name: string;
  icon: string;
  color: string;
  earnedAt: string;
}

export interface TimeStats {
  totalTime: number;
  averageSessionTime: number;
  averageTimePerExercise: number;
  totalSessions: number;
}
