// Core Types for Spanish Subjunctive Practice App
// Note: For API types, use types from @/types/api.ts instead

export interface User {
  id: number; // Changed from string to match backend
  email: string;
  username: string;
  createdAt: Date;
  preferences: UserPreferences;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'high-contrast';
  fontSize: 'small' | 'medium' | 'large' | 'xl';
  reducedMotion: boolean;
  language: 'en' | 'es';
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export interface Exercise {
  id: string;
  type: 'fill-blank' | 'multiple-choice' | 'conjugation' | 'translation';
  verb: string;
  tense: string;
  sentence: string;
  blanks: string[];
  options?: string[];
  correctAnswer: string | string[];
  explanation: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  hints: string[];
}

export interface PracticeSession {
  id: string;
  userId: string;
  startTime: Date;
  endTime?: Date;
  exercises: Exercise[];
  currentIndex: number;
  answers: Answer[];
  score: number;
  completed: boolean;
  settings: SessionSettings;
}

export interface Answer {
  exerciseId: string;
  userAnswer: string | string[];
  isCorrect: boolean;
  hintsUsed: number;
  timeSpent: number;
  submittedAt: Date;
}

export interface SessionSettings {
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  timeLimit?: number;
  hintsEnabled: boolean;
  feedbackType: 'immediate' | 'end';
  exerciseCount: number;
}

export interface Statistics {
  totalExercises: number;
  correctAnswers: number;
  accuracy: number;
  currentStreak: number;
  longestStreak: number;
  averageTimePerExercise: number;
  verbsMastered: string[];
  weakAreas: string[];
  lastPracticeDate: Date;
  totalPracticeTime: number;
  level: number;
  xp: number;
  achievements: Achievement[];
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlockedAt?: Date;
  progress: number;
  target: number;
}

export interface ProgressData {
  date: Date;
  exercisesCompleted: number;
  accuracy: number;
  timeSpent: number;
}

export interface ToastNotification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
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

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  loading?: boolean;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
  ariaLabel?: string;
}

export interface InputProps {
  id: string;
  name: string;
  label: string;
  type?: 'text' | 'email' | 'password' | 'number';
  value: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  error?: string;
  helpText?: string;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  autoComplete?: string;
  className?: string;
}

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showCloseButton?: boolean;
  closeOnOverlayClick?: boolean;
}

export interface CardProps {
  children: React.ReactNode;
  className?: string;
  elevated?: boolean;
  interactive?: boolean;
  onClick?: () => void;
}
