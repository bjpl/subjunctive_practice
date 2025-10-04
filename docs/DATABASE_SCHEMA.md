# Database Schema Documentation

## Overview

The Spanish Subjunctive Practice application uses a PostgreSQL/SQLite database with SQLAlchemy ORM for data management. The schema is designed to support user management, exercise content, progress tracking, and spaced repetition learning.

## Schema Organization

### User Management
- **users** - Core user accounts
- **user_profiles** - User learning profiles and streaks
- **user_preferences** - User settings and preferences

### Exercise Content
- **verbs** - Spanish verbs with conjugations
- **exercises** - Practice exercises
- **scenarios** - Themed exercise collections
- **exercise_scenarios** - Many-to-many relationship

### Progress Tracking
- **sessions** - Practice sessions
- **attempts** - Individual exercise attempts
- **achievements** - Available achievements
- **user_achievements** - User-earned achievements
- **review_schedules** - Spaced repetition schedules
- **user_statistics** - Aggregated user statistics

## Entity Relationship Diagram

```
Users (1) ─── (1) UserProfiles
  │
  ├── (1) ─── (1) UserPreferences
  │
  ├── (1) ─── (N) Sessions
  │              └── (1) ─── (N) Attempts
  │
  ├── (1) ─── (N) UserAchievements ─── (N) Achievements
  │
  ├── (1) ─── (N) ReviewSchedules ─── (N) Verbs
  │
  └── (1) ─── (1) UserStatistics

Verbs (1) ─── (N) Exercises ─── (N) ExerciseScenarios ─── (N) Scenarios
```

## Table Details

### Users Table
Primary user account information.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('student', 'teacher', 'admin') DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

**Indexes:** username, email

### User Profiles Table
Extended user information for learning.

```sql
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(100),
    avatar_url VARCHAR(500),
    bio TEXT,
    current_level ENUM('A1','A2','B1','B2','C1','C2') DEFAULT 'A1',
    target_level ENUM('A1','A2','B1','B2','C1','C2'),
    native_language VARCHAR(50) DEFAULT 'English',
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_practice_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### User Preferences Table
User settings and learning preferences.

```sql
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    daily_goal INTEGER DEFAULT 10,
    session_length INTEGER DEFAULT 15,
    difficulty_preference INTEGER DEFAULT 2,
    email_notifications BOOLEAN DEFAULT TRUE,
    reminder_enabled BOOLEAN DEFAULT TRUE,
    reminder_time VARCHAR(5) DEFAULT '19:00',
    show_explanations BOOLEAN DEFAULT TRUE,
    auto_advance BOOLEAN DEFAULT FALSE,
    audio_enabled BOOLEAN DEFAULT TRUE,
    enable_spaced_repetition BOOLEAN DEFAULT TRUE,
    review_frequency INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Verbs Table
Spanish verbs with subjunctive conjugations.

```sql
CREATE TABLE verbs (
    id INTEGER PRIMARY KEY,
    infinitive VARCHAR(50) UNIQUE NOT NULL,
    english_translation VARCHAR(100) NOT NULL,
    verb_type ENUM('regular','irregular','stem_changing','reflexive') NOT NULL,
    present_subjunctive JSON NOT NULL,  -- {yo: "hable", tú: "hables", ...}
    imperfect_subjunctive_ra JSON,
    imperfect_subjunctive_se JSON,
    frequency_rank INTEGER,
    is_irregular BOOLEAN DEFAULT FALSE,
    irregularity_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:** infinitive, verb_type

**Seed Data:** 20 common Spanish verbs including:
- ser, estar, tener, hacer, poder, ir, ver, dar, saber, querer
- hablar, vivir, pensar, venir, decir, encontrar, pedir, sentir, dormir, creer, estudiar

### Exercises Table
Practice exercises for subjunctive forms.

```sql
CREATE TABLE exercises (
    id INTEGER PRIMARY KEY,
    verb_id INTEGER REFERENCES verbs(id) ON DELETE CASCADE,
    exercise_type ENUM('fill_blank','multiple_choice','conjugation','translation','trigger_identification') NOT NULL,
    tense ENUM('present_subjunctive','imperfect_subjunctive','present_perfect_subjunctive','pluperfect_subjunctive') NOT NULL,
    difficulty ENUM(1,2,3,4) NOT NULL,  -- Easy, Medium, Hard, Expert
    prompt TEXT NOT NULL,
    correct_answer VARCHAR(200) NOT NULL,
    alternative_answers JSON,  -- ["fuese", "fuera"]
    distractors JSON,  -- For multiple choice
    explanation TEXT,
    trigger_phrase VARCHAR(100),
    hint TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    usage_count INTEGER DEFAULT 0,
    success_rate INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:** verb_id, exercise_type, tense, difficulty

### Scenarios Table
Themed exercise collections.

```sql
CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    theme VARCHAR(50) NOT NULL,  -- travel, work, relationships
    context TEXT,
    image_url VARCHAR(500),
    recommended_level VARCHAR(2),  -- A1, B2, etc.
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Exercise Scenarios Table (Junction)
Many-to-many relationship between exercises and scenarios.

```sql
CREATE TABLE exercise_scenarios (
    id INTEGER PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises(id) ON DELETE CASCADE,
    scenario_id INTEGER REFERENCES scenarios(id) ON DELETE CASCADE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:** exercise_id, scenario_id

### Sessions Table
Practice session tracking.

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    duration_seconds INTEGER,
    total_exercises INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    score_percentage FLOAT,
    session_type VARCHAR(50) DEFAULT 'practice',  -- practice, review, test
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:** user_id

### Attempts Table
Individual exercise attempt details.

```sql
CREATE TABLE attempts (
    id INTEGER PRIMARY KEY,
    session_id INTEGER REFERENCES sessions(id) ON DELETE CASCADE,
    exercise_id INTEGER REFERENCES exercises(id) ON DELETE SET NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    user_answer VARCHAR(200) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INTEGER,
    hints_used INTEGER DEFAULT 0,
    attempts_count INTEGER DEFAULT 1,
    confidence_level INTEGER,  -- 1-5
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:** session_id, exercise_id, user_id

### Achievements Table
Available achievements and badges.

```sql
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,  -- streak, mastery, practice, milestone
    icon_url VARCHAR(500),
    points INTEGER DEFAULT 10,
    criteria JSON NOT NULL,  -- {"streak_days": 7}
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Seed Data:** 5 achievements including:
- First Steps (1 exercise)
- Week Warrior (7-day streak)
- Century Club (100 correct answers)
- Perfect Session (100% accuracy)
- Subjunctive Master (20 verbs mastered)

### User Achievements Table
User-earned achievements.

```sql
CREATE TABLE user_achievements (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    achievement_id INTEGER REFERENCES achievements(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP DEFAULT NOW(),
    progress_data JSON,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:** user_id, achievement_id

### Review Schedules Table
Spaced repetition using SM-2 algorithm.

```sql
CREATE TABLE review_schedules (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    verb_id INTEGER REFERENCES verbs(id) ON DELETE CASCADE,
    easiness_factor FLOAT DEFAULT 2.5,  -- 1.3 - 2.5
    interval_days INTEGER DEFAULT 1,
    repetitions INTEGER DEFAULT 0,
    next_review_date TIMESTAMP NOT NULL,
    last_reviewed_at TIMESTAMP,
    review_count INTEGER DEFAULT 0,
    total_correct INTEGER DEFAULT 0,
    total_attempts INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:** user_id, verb_id

### User Statistics Table
Aggregated analytics (updated periodically).

```sql
CREATE TABLE user_statistics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    total_sessions INTEGER DEFAULT 0,
    total_exercises_completed INTEGER DEFAULT 0,
    total_correct_answers INTEGER DEFAULT 0,
    overall_accuracy FLOAT DEFAULT 0.0,
    total_study_time_minutes INTEGER DEFAULT 0,
    average_session_duration INTEGER DEFAULT 0,
    verbs_mastered INTEGER DEFAULT 0,
    verbs_learning INTEGER DEFAULT 0,
    weekly_exercises INTEGER DEFAULT 0,
    weekly_accuracy FLOAT DEFAULT 0.0,
    total_achievements INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    last_calculated_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes:** user_id

## Key Design Decisions

### 1. Database Engine Support
- **Primary:** PostgreSQL (production)
- **Secondary:** SQLite (development/testing)
- Foreign key constraints enabled for both
- Connection pooling configured for PostgreSQL

### 2. Timestamp Management
- All tables include `created_at` and `updated_at`
- Automatic timestamp updates via SQLAlchemy `onupdate`
- UTC timestamps for consistency

### 3. Soft Deletes
- User accounts use `is_active` flag
- Exercises use `is_active` flag
- Cascade deletes for dependent data

### 4. JSON Storage
- Verb conjugations (flexible structure)
- Exercise distractors and alternatives
- Achievement criteria
- Progress metadata

### 5. Enumerations
- User roles (student, teacher, admin)
- Language levels (CEFR: A1-C2)
- Verb types (regular, irregular, etc.)
- Exercise types and difficulties
- Subjunctive tenses

### 6. Indexing Strategy
- Primary keys on all tables
- Foreign keys for relationships
- Unique constraints on usernames/emails
- Composite indexes on frequently queried fields

### 7. Spaced Repetition (SM-2 Algorithm)
- Tracks easiness factor (1.3-2.5)
- Interval-based review scheduling
- Performance tracking per verb

## Migration Management

### Alembic Setup

```bash
# Create migration
cd backend
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1

# View history
alembic history
```

### Database Initialization

```bash
# Initialize database with seed data
python scripts/init_db.py

# Reset database (WARNING: destroys all data)
python scripts/init_db.py --reset

# Initialize without seed data
python scripts/init_db.py --no-seed
```

## File Locations

### SQLAlchemy Models
- `backend/models/user.py` - User, UserProfile, UserPreference
- `backend/models/exercise.py` - Verb, Exercise, Scenario, ExerciseScenario
- `backend/models/progress.py` - Session, Attempt, Achievement, ReviewSchedule, UserStatistics

### Pydantic Schemas
- `backend/schemas/user.py` - User validation schemas
- `backend/schemas/exercise.py` - Exercise validation schemas
- `backend/schemas/progress.py` - Progress validation schemas

### Database Configuration
- `backend/core/database.py` - Database connection and session management
- `backend/core/seed_data.py` - Initial verbs and achievements

### Migrations
- `backend/alembic/` - Alembic migration scripts
- `backend/alembic.ini` - Alembic configuration

## Performance Considerations

1. **Connection Pooling**: PostgreSQL uses 10 connections with 20 overflow
2. **Eager Loading**: Use `joinedload()` for related data
3. **Batch Operations**: Bulk insert for seed data
4. **Statistics Caching**: `user_statistics` table for aggregated queries
5. **Index Coverage**: All foreign keys and frequently queried fields indexed

## Security Features

1. **Password Hashing**: bcrypt via passlib
2. **Foreign Key Constraints**: Prevent orphaned records
3. **Input Validation**: Pydantic schemas for all API inputs
4. **SQL Injection Prevention**: SQLAlchemy parameterized queries
5. **Cascade Deletes**: Proper cleanup of dependent data
