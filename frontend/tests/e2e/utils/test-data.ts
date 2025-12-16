/**
 * Test data for E2E tests
 */

export const testUsers = {
  default: {
    email: 'test@example.com',
    username: 'testuser',
    password: 'Password123!',
  },
  existing: {
    email: 'existing@example.com',
    username: 'existinguser',
    password: 'Password123!',
  },
  admin: {
    email: 'admin@example.com',
    username: 'admin',
    password: 'AdminPassword123!',
  },
};

export const testExercises = {
  present: {
    id: 1,
    verb: 'hablar',
    tense: 'present',
    person: 'first',
    number: 'singular',
    correctAnswer: 'hable',
    incorrectAnswers: ['hablo', 'habla', 'hablas'],
    explanation: 'Present subjunctive of hablar, yo form',
  },
  imperfect: {
    id: 2,
    verb: 'comer',
    tense: 'imperfect',
    person: 'second',
    number: 'singular',
    correctAnswer: 'comieras',
    incorrectAnswers: ['comes', 'comías', 'comas'],
    explanation: 'Imperfect subjunctive of comer, tú form',
  },
  future: {
    id: 3,
    verb: 'vivir',
    tense: 'future',
    person: 'third',
    number: 'plural',
    correctAnswer: 'vivieren',
    incorrectAnswers: ['vivirán', 'vivan', 'vivieran'],
    explanation: 'Future subjunctive of vivir, ellos form',
  },
};

export const practiceSettings = {
  default: {
    difficulty: 'intermediate',
    tense: 'all',
    exerciseCount: 10,
    timeLimit: null,
  },
  beginner: {
    difficulty: 'beginner',
    tense: 'present',
    exerciseCount: 5,
    timeLimit: null,
  },
  advanced: {
    difficulty: 'advanced',
    tense: 'all',
    exerciseCount: 20,
    timeLimit: 30 * 60, // 30 minutes in seconds
  },
  quick: {
    difficulty: 'intermediate',
    tense: 'present',
    exerciseCount: 3,
    timeLimit: null,
  },
  custom: {
    difficulty: 'intermediate',
    tense: 'imperfect',
    exerciseCount: 15,
    timeLimit: 15 * 60,
  },
};

export const userProgress = {
  beginner: {
    totalExercises: 25,
    correctAnswers: 18,
    accuracy: 72,
    currentStreak: 3,
    longestStreak: 7,
    totalPoints: 180,
    level: 2,
    weakAreas: ['imperfect', 'future'],
  },
  intermediate: {
    totalExercises: 150,
    correctAnswers: 128,
    accuracy: 85,
    currentStreak: 12,
    longestStreak: 15,
    totalPoints: 1280,
    level: 5,
    weakAreas: ['pluperfect'],
  },
  advanced: {
    totalExercises: 500,
    correctAnswers: 460,
    accuracy: 92,
    currentStreak: 30,
    longestStreak: 45,
    totalPoints: 4600,
    level: 10,
    weakAreas: [],
  },
};

export const achievements = {
  firstSteps: {
    id: 'first_steps',
    name: 'First Steps',
    description: 'Complete your first practice session',
    icon: '🎯',
    unlocked: true,
    unlockedAt: '2024-01-15T10:30:00Z',
  },
  weekWarrior: {
    id: 'week_warrior',
    name: 'Week Warrior',
    description: 'Practice for 7 days in a row',
    icon: '🔥',
    unlocked: true,
    unlockedAt: '2024-01-22T18:45:00Z',
  },
  perfectScore: {
    id: 'perfect_score',
    name: 'Perfect Score',
    description: 'Get 100% accuracy in a session with 10+ exercises',
    icon: '💯',
    unlocked: false,
    unlockedAt: null,
  },
  centurion: {
    id: 'centurion',
    name: 'Centurion',
    description: 'Complete 100 practice exercises',
    icon: '🏆',
    unlocked: true,
    unlockedAt: '2024-02-01T12:00:00Z',
  },
  subjunctiveMaster: {
    id: 'subjunctive_master',
    name: 'Subjunctive Master',
    description: 'Achieve 95% accuracy across all tenses',
    icon: '👑',
    unlocked: false,
    unlockedAt: null,
  },
};

export const mockSessionResults = {
  perfect: {
    exercisesCompleted: 10,
    correctAnswers: 10,
    incorrectAnswers: 0,
    skipped: 0,
    accuracy: 100,
    pointsEarned: 100,
    timeElapsed: 180, // 3 minutes
    tenseDistribution: {
      present: 5,
      imperfect: 3,
      future: 2,
    },
  },
  good: {
    exercisesCompleted: 10,
    correctAnswers: 8,
    incorrectAnswers: 2,
    skipped: 0,
    accuracy: 80,
    pointsEarned: 80,
    timeElapsed: 240,
    tenseDistribution: {
      present: 6,
      imperfect: 4,
    },
  },
  needsWork: {
    exercisesCompleted: 10,
    correctAnswers: 5,
    incorrectAnswers: 4,
    skipped: 1,
    accuracy: 50,
    pointsEarned: 50,
    timeElapsed: 420,
    tenseDistribution: {
      present: 3,
      imperfect: 4,
      future: 2,
      pluperfect: 1,
    },
  },
};

export const errorMessages = {
  auth: {
    invalidCredentials: 'Invalid email or password',
    emailExists: 'Email already exists',
    passwordMismatch: 'Passwords do not match',
    weakPassword: 'Password must be at least 8 characters',
    requiredEmail: 'Email is required',
    requiredPassword: 'Password is required',
    requiredUsername: 'Username is required',
  },
  practice: {
    emptyAnswer: 'Please enter an answer',
    sessionExpired: 'Your session has expired',
    noExercises: 'No exercises available for the selected criteria',
  },
  settings: {
    updateFailed: 'Failed to update settings',
    invalidDailyGoal: 'Daily goal must be between 1 and 100',
  },
};

export const routes = {
  home: '/',
  login: '/auth/login',
  register: '/auth/register',
  dashboard: '/dashboard',
  practice: '/practice',
  progress: '/progress',
  settings: '/settings',
  review: '/review',
};

/**
 * Generate a unique email address for testing
 */
export function generateUniqueEmail(): string {
  return `test${Date.now()}@example.com`;
}

/**
 * Generate a unique username for testing
 */
export function generateUniqueUsername(): string {
  return `user${Date.now()}`;
}

/**
 * Create a test user with unique credentials
 */
export function createUniqueTestUser() {
  return {
    email: generateUniqueEmail(),
    username: generateUniqueUsername(),
    password: 'Password123!',
  };
}
