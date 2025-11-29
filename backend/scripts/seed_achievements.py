"""
Seed achievements database with initial achievement definitions.

This script creates all achievements matching the frontend definitions
in frontend/lib/gamification.ts.

Usage:
    python -m scripts.seed_achievements
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from core.database import get_db, init_db
from models.progress import Achievement
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Achievement definitions matching frontend/lib/gamification.ts
ACHIEVEMENT_DEFINITIONS = [
    # Streak achievements
    {
        "name": "Getting Started",
        "description": "Practice for 3 days in a row",
        "category": "streak",
        "icon_url": "flame",
        "points": 10,
        "criteria": {"streak_days": 3}
    },
    {
        "name": "Week Warrior",
        "description": "Practice for 7 days in a row",
        "category": "streak",
        "icon_url": "flame",
        "points": 25,
        "criteria": {"streak_days": 7}
    },
    {
        "name": "Month Master",
        "description": "Practice for 30 days in a row",
        "category": "streak",
        "icon_url": "flame",
        "points": 100,
        "criteria": {"streak_days": 30}
    },
    {
        "name": "Century Champion",
        "description": "Practice for 100 days in a row",
        "category": "streak",
        "icon_url": "flame",
        "points": 500,
        "criteria": {"streak_days": 100}
    },

    # Accuracy achievements
    {
        "name": "Perfect Ten",
        "description": "Get 10 exercises correct in a row",
        "category": "accuracy",
        "icon_url": "target",
        "points": 15,
        "criteria": {"correct_answers": 10}
    },
    {
        "name": "Sharpshooter",
        "description": "Get 25 exercises correct in a row",
        "category": "accuracy",
        "icon_url": "target",
        "points": 50,
        "criteria": {"correct_answers": 25}
    },
    {
        "name": "Perfectionist",
        "description": "Get 50 exercises correct in a row",
        "category": "accuracy",
        "icon_url": "target",
        "points": 150,
        "criteria": {"correct_answers": 50}
    },
    {
        "name": "Flawless Victory",
        "description": "Complete a session with 100% accuracy",
        "category": "accuracy",
        "icon_url": "award",
        "points": 30,
        "criteria": {"perfect_session": True, "perfect_sessions": 1}
    },

    # Volume achievements
    {
        "name": "Dedicated Learner",
        "description": "Complete 50 exercises",
        "category": "volume",
        "icon_url": "book-open",
        "points": 20,
        "criteria": {"exercises_completed": 50}
    },
    {
        "name": "Practice Makes Perfect",
        "description": "Complete 250 exercises",
        "category": "volume",
        "icon_url": "book-open",
        "points": 75,
        "criteria": {"exercises_completed": 250}
    },
    {
        "name": "Master Student",
        "description": "Complete 1,000 exercises",
        "category": "volume",
        "icon_url": "book-open",
        "points": 250,
        "criteria": {"exercises_completed": 1000}
    },
    {
        "name": "Grammar Guru",
        "description": "Complete 5,000 exercises",
        "category": "volume",
        "icon_url": "book-open",
        "points": 1000,
        "criteria": {"exercises_completed": 5000}
    },

    # Mastery achievements
    {
        "name": "Topic Master",
        "description": "Achieve 90% accuracy in any category",
        "category": "mastery",
        "icon_url": "graduation-cap",
        "points": 100,
        "criteria": {"accuracy_threshold": 90}
    },
    {
        "name": "Complete Mastery",
        "description": "Achieve 85% accuracy in all categories",
        "category": "mastery",
        "icon_url": "trophy",
        "points": 500,
        "criteria": {"all_categories": True, "accuracy_threshold": 85}
    },

    # Special achievements
    {
        "name": "Speed Demon",
        "description": "Complete 20 exercises in under 5 minutes",
        "category": "special",
        "icon_url": "zap",
        "points": 75,
        "criteria": {"type": "speed_demon", "exercises": 20, "time_seconds": 300}
    },
    {
        "name": "Night Owl",
        "description": "Practice between midnight and 4 AM",
        "category": "special",
        "icon_url": "moon",
        "points": 10,
        "criteria": {"type": "night_owl"}
    },
    {
        "name": "Early Bird",
        "description": "Practice between 5 AM and 7 AM",
        "category": "special",
        "icon_url": "sunrise",
        "points": 10,
        "criteria": {"type": "early_bird"}
    },
]


def seed_achievements(db: Session) -> None:
    """
    Seed the achievements table with initial data.

    Args:
        db: Database session
    """
    logger.info("Starting achievement seeding...")

    # Check for existing achievements
    existing_count = db.query(Achievement).count()
    if existing_count > 0:
        logger.warning(f"Found {existing_count} existing achievements. Skipping duplicates.")

    created_count = 0
    skipped_count = 0

    for ach_data in ACHIEVEMENT_DEFINITIONS:
        # Check if achievement already exists by name
        existing = db.query(Achievement).filter(
            Achievement.name == ach_data["name"]
        ).first()

        if existing:
            logger.info(f"Skipping existing achievement: {ach_data['name']}")
            skipped_count += 1
            continue

        # Create new achievement
        achievement = Achievement(
            name=ach_data["name"],
            description=ach_data["description"],
            category=ach_data["category"],
            icon_url=ach_data["icon_url"],
            points=ach_data["points"],
            criteria=ach_data["criteria"]
        )
        db.add(achievement)
        created_count += 1
        logger.info(f"Created achievement: {ach_data['name']} ({ach_data['category']}, {ach_data['points']} pts)")

    # Commit all achievements
    db.commit()

    logger.info(f"Achievement seeding complete!")
    logger.info(f"  Created: {created_count}")
    logger.info(f"  Skipped: {skipped_count}")
    logger.info(f"  Total: {created_count + skipped_count}")


def main():
    """Main entry point for achievement seeding script."""
    logger.info("Initializing database...")

    # Initialize database and get session
    init_db()
    db = next(get_db())

    try:
        seed_achievements(db)
        logger.info("✓ Achievement seeding successful!")
        return 0
    except Exception as e:
        logger.error(f"✗ Achievement seeding failed: {e}", exc_info=True)
        db.rollback()
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
