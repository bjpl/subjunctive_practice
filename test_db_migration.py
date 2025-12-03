#!/usr/bin/env python3
"""
Test script to verify database migration is working.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.exercise import Exercise, DifficultyLevel, SubjunctiveTense

# Create engine
DATABASE_URL = "sqlite:///./subjunctive_practice.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def test_database_exercises():
    """Test that exercises can be queried from database."""
    print("=" * 60)
    print("DATABASE MIGRATION TEST")
    print("=" * 60)

    db = SessionLocal()
    try:
        # Count total exercises
        total = db.query(Exercise).count()
        print(f"\nTotal exercises in database: {total}")

        # Count by difficulty
        print("\nExercises by difficulty:")
        for diff in DifficultyLevel:
            count = db.query(Exercise).filter(Exercise.difficulty == diff).count()
            print(f"  {diff.name} (level {diff.value}): {count}")

        # Count by tense
        print("\nExercises by tense:")
        for tense in SubjunctiveTense:
            count = db.query(Exercise).filter(Exercise.tense == tense).count()
            print(f"  {tense.value}: {count}")

        # Sample exercises
        print("\nSample exercises:")
        samples = db.query(Exercise).limit(5).all()
        for ex in samples:
            print(f"\n  ID: {ex.id}")
            print(f"  Difficulty: {ex.difficulty.name} ({ex.difficulty.value})")
            print(f"  Tense: {ex.tense.value}")
            print(f"  Prompt: {ex.prompt[:60]}...")
            print(f"  Answer: {ex.correct_answer}")

        # Test filtering
        print("\n" + "=" * 60)
        print("TESTING FILTERS")
        print("=" * 60)

        # Test difficulty filter
        easy_exercises = db.query(Exercise).filter(
            Exercise.difficulty == DifficultyLevel.EASY
        ).all()
        print(f"\nEasy exercises: {len(easy_exercises)}")

        # Test tense filter
        present_subj = db.query(Exercise).filter(
            Exercise.tense == SubjunctiveTense.PRESENT
        ).all()
        print(f"Present subjunctive exercises: {len(present_subj)}")

        # Test active filter
        active = db.query(Exercise).filter(Exercise.is_active == True).count()
        print(f"Active exercises: {active}")

        print("\n" + "=" * 60)
        print("MIGRATION TEST PASSED ✅")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_database_exercises()
    sys.exit(0 if success else 1)
