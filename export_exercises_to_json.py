#!/usr/bin/env python3
"""
Export database exercises to JSON format for fallback API.
Temporary script until exercises router is updated to use database directly.
"""

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models.exercise import Exercise, DifficultyLevel, ExerciseType, SubjunctiveTense, Verb
from models.progress import ReviewSchedule, Attempt  # Import for SQLAlchemy relationship resolution
from models.user import User  # Import for SQLAlchemy relationship resolution
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_exercises_to_json():
    """Export exercises from database to JSON file."""
    db: Session = SessionLocal()

    try:
        # Query all exercises
        exercises = db.query(Exercise).all()

        if not exercises:
            logger.warning("No exercises found in database")
            return

        # Convert to JSON format expected by exercises router
        exercises_json = []
        for ex in exercises:
            exercise_dict = {
                "id": str(ex.id),
                "type": ex.exercise_type.value if ex.exercise_type else "fill_blank",
                "prompt": ex.prompt,
                "difficulty": ex.difficulty.value if ex.difficulty else 3,
                "answer": ex.correct_answer,
                "explanation": ex.explanation if ex.explanation else "",
                "hints": [ex.hint] if ex.hint else [],
                "tags": [ex.trigger_phrase] if ex.trigger_phrase else [],
                "trigger_phrase": ex.trigger_phrase if ex.trigger_phrase else ""
            }
            exercises_json.append(exercise_dict)

        # Write to JSON file
        output = {
            "subjunctive_exercises": exercises_json,
            "total_count": len(exercises_json),
            "exported_at": "2025-10-07T00:00:00Z"
        }

        with open("user_data/fallback_exercises.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Exported {len(exercises_json)} exercises to user_data/fallback_exercises.json")

        # Print sample
        if exercises_json:
            logger.info(f"\nSample exercise:")
            logger.info(json.dumps(exercises_json[0], indent=2, ensure_ascii=False))

    except Exception as e:
        logger.error(f"❌ Export failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    export_exercises_to_json()
