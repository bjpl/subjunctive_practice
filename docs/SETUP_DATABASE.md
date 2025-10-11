# Database Setup Guide

## Prerequisites

1. Python 3.10 or higher
2. PostgreSQL 14+ (for production) OR SQLite (for development)
3. Virtual environment activated

## Installation

### 1. Install Python Dependencies

```bash
# From project root
cd backend
pip install -r requirements.txt
```

Required packages:
- `sqlalchemy==2.0.27` - ORM
- `alembic==1.13.1` - Migrations
- `psycopg2-binary==2.9.9` - PostgreSQL driver
- `pydantic==2.6.1` - Data validation
- `email-validator` - Email validation for Pydantic

### 2. Configure Database Connection

Create or edit `.env` file in project root:

```bash
# SQLite (Development)
DATABASE_URL=sqlite:///./subjunctive_practice.db

# OR PostgreSQL (Production)
DATABASE_URL=postgresql://username:password@localhost:5432/subjunctive_practice
```

### 3. Initialize Database

#### Option A: Quick Setup (with seed data)

```bash
python scripts/init_db.py
```

This will:
- Create all tables
- Seed 20 common Spanish verbs
- Create 5 initial achievements

#### Option B: Manual Setup

```bash
# Just create tables (no seed data)
python scripts/init_db.py --no-seed

# Reset database (WARNING: destroys all data!)
python scripts/init_db.py --reset
```

## Using Alembic Migrations

### First Time Setup

The alembic configuration is already created. To generate the initial migration:

```bash
cd backend

# Generate migration from models
alembic revision --autogenerate -m "Initial database schema"

# Apply migration
alembic upgrade head
```

### Common Migration Commands

```bash
cd backend

# Create a new migration after model changes
alembic revision --autogenerate -m "Add new field to User model"

# Apply all pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# View migration history
alembic history

# View current database version
alembic current

# View SQL without executing
alembic upgrade head --sql
```

## Database Structure

The database includes 13 tables:

### User Management (3 tables)
- `users` - Core user accounts
- `user_profiles` - Learning profiles and streaks
- `user_preferences` - User settings

### Exercise Content (4 tables)
- `verbs` - Spanish verbs with conjugations
- `exercises` - Practice exercises
- `scenarios` - Themed collections
- `exercise_scenarios` - Junction table

### Progress Tracking (6 tables)
- `sessions` - Practice sessions
- `attempts` - Individual exercise attempts
- `achievements` - Available achievements
- `user_achievements` - Earned achievements
- `review_schedules` - Spaced repetition
- `user_statistics` - Aggregated stats

## Seed Data

### Verbs (20 included)

Common Spanish verbs with subjunctive conjugations:
- **Irregular:** ser, estar, tener, hacer, poder, ir, ver, dar, saber, querer, venir, decir
- **Stem-changing:** pensar, encontrar, pedir, sentir, dormir
- **Regular:** hablar, vivir, creer, estudiar

Each verb includes:
- Present subjunctive (all persons)
- Imperfect subjunctive (-ra and -se forms)
- English translation
- Verb type classification
- Frequency ranking
- Irregularity notes

### Achievements (5 included)

1. **First Steps** - Complete first exercise (10 points)
2. **Week Warrior** - 7-day streak (50 points)
3. **Century Club** - 100 correct answers (100 points)
4. **Perfect Session** - 100% in 10+ exercises (25 points)
5. **Subjunctive Master** - Master 20 verbs (200 points)

## Testing the Database

### Using Python Shell

```python
from backend.core.database import get_db
from backend.models import User, Verb, Exercise

# Create a session
with get_db() as db:
    # Query verbs
    verbs = db.query(Verb).all()
    print(f"Found {len(verbs)} verbs")

    # Find irregular verbs
    irregular = db.query(Verb).filter(Verb.is_irregular == True).all()
    for verb in irregular:
        print(f"{verb.infinitive} - {verb.english_translation}")
```

### Using psql (PostgreSQL)

```bash
# Connect to database
psql -U username -d subjunctive_practice

# List tables
\dt

# View users
SELECT * FROM users LIMIT 10;

# View verbs
SELECT infinitive, english_translation, verb_type FROM verbs ORDER BY frequency_rank;

# View exercises by difficulty
SELECT difficulty, COUNT(*) FROM exercises GROUP BY difficulty;
```

### Using sqlite3 (SQLite)

```bash
# Connect to database
sqlite3 subjunctive_practice.db

# List tables
.tables

# View schema
.schema users

# Query data
SELECT * FROM verbs LIMIT 10;

# Exit
.exit
```

## Troubleshooting

### Error: "No module named 'email_validator'"

```bash
pip install email-validator
# OR
pip install pydantic[email]
```

### Error: "No such table"

```bash
# Reinitialize database
python scripts/init_db.py
```

### Error: "Database is locked" (SQLite)

SQLite doesn't support concurrent writes well. For production, use PostgreSQL.

### Error: Import errors

Make sure you're running from the project root and the backend directory is in your Python path:

```bash
# From project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python scripts/init_db.py
```

### PostgreSQL Connection Issues

```bash
# Check PostgreSQL is running
pg_isready

# Start PostgreSQL (Linux/Mac)
sudo systemctl start postgresql

# Start PostgreSQL (Windows)
# Use pg_ctl or Services panel
```

## Database Maintenance

### Backup (PostgreSQL)

```bash
pg_dump -U username subjunctive_practice > backup.sql
```

### Restore (PostgreSQL)

```bash
psql -U username subjunctive_practice < backup.sql
```

### Backup (SQLite)

```bash
# Simple copy
cp subjunctive_practice.db subjunctive_practice.db.backup

# Or using SQLite
sqlite3 subjunctive_practice.db ".backup backup.db"
```

### Reset Development Database

```bash
python scripts/init_db.py --reset
```

## Next Steps

After database setup:

1. **Create API endpoints** - `backend/api/` directory
2. **Add authentication** - JWT tokens with python-jose
3. **Implement spaced repetition** - Review schedule logic
4. **Add analytics** - Statistics calculation
5. **Create admin panel** - Exercise management

## Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
