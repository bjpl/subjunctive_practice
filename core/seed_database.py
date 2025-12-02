#!/usr/bin/env python3
"""
Database seeding script for Spanish Subjunctive Practice application.

This script populates the database with:
- Verbs with conjugations
- Exercises organized by difficulty
- Scenarios for contextual learning
- Achievements for gamification

Usage:
    python backend/core/seed_database.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from models.exercise import Verb, Exercise, Scenario, ExerciseScenario
from models.progress import ReviewSchedule, Attempt  # Import related models for SQLAlchemy
from models.user import User  # Import related models
from core.seed_data import SEED_VERBS, SEED_ACHIEVEMENTS
from core.comprehensive_seed_data import SEED_EXERCISES, SEED_SCENARIOS
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def seed_verbs(db: Session) -> dict:
    """
    Seed Spanish verbs with conjugations.
    Returns dict mapping infinitive → Verb object.
    """
    logger.info("Seeding verbs...")
    verb_map = {}

    for verb_data in SEED_VERBS:
        # Check if verb already exists
        existing = db.query(Verb).filter(Verb.infinitive == verb_data["infinitive"]).first()
        if existing:
            logger.debug(f"Verb '{verb_data['infinitive']}' already exists, skipping")
            verb_map[verb_data["infinitive"]] = existing
            continue

        # Create new verb
        verb = Verb(
            infinitive=verb_data["infinitive"],
            english_translation=verb_data["english_translation"],
            verb_type=verb_data["verb_type"],
            present_subjunctive=verb_data["present_subjunctive"],
            imperfect_subjunctive_ra=verb_data.get("imperfect_subjunctive_ra"),
            imperfect_subjunctive_se=verb_data.get("imperfect_subjunctive_se"),
            frequency_rank=verb_data.get("frequency_rank"),
            is_irregular=verb_data.get("is_irregular", False),
            irregularity_notes=verb_data.get("irregularity_notes")
        )
        db.add(verb)
        verb_map[verb_data["infinitive"]] = verb
        logger.debug(f"Added verb: {verb_data['infinitive']}")

    db.commit()
    logger.info(f"✅ Seeded {len(verb_map)} verbs")
    return verb_map


def seed_exercises(db: Session, verb_map: dict) -> list:
    """
    Seed exercises linking to verbs.
    Returns list of Exercise objects.
    """
    logger.info("Seeding exercises...")
    exercises = []
    skipped = 0

    for exercise_data in SEED_EXERCISES:
        verb_infinitive = exercise_data["verb_infinitive"]

        # Get verb from map
        if verb_infinitive not in verb_map:
            logger.warning(f"Verb '{verb_infinitive}' not found, skipping exercise")
            skipped += 1
            continue

        verb = verb_map[verb_infinitive]

        # Check if exact exercise already exists (by prompt)
        existing = db.query(Exercise).filter(
            Exercise.prompt == exercise_data["prompt"]
        ).first()
        if existing:
            logger.debug(f"Exercise already exists: {exercise_data['prompt'][:50]}...")
            exercises.append(existing)
            continue

        # Create exercise
        exercise = Exercise(
            verb_id=verb.id,
            exercise_type=exercise_data["exercise_type"],
            tense=exercise_data["tense"],
            difficulty=exercise_data["difficulty"],
            prompt=exercise_data["prompt"],
            correct_answer=exercise_data["correct_answer"],
            alternative_answers=exercise_data.get("alternative_answers", []),
            distractors=exercise_data.get("distractors", []),
            explanation=exercise_data.get("explanation"),
            trigger_phrase=exercise_data.get("trigger_phrase"),
            hint=exercise_data.get("hint"),
            tags=exercise_data.get("tags", []),
            is_active=True,
            usage_count=0,
            success_rate=0
        )
        db.add(exercise)
        exercises.append(exercise)
        logger.debug(f"Added exercise: {exercise_data['trigger_phrase']} - {verb_infinitive}")

    db.commit()
    logger.info(f"✅ Seeded {len(exercises)} exercises ({skipped} skipped)")
    return exercises


def seed_scenarios(db: Session) -> dict:
    """
    Seed learning scenarios (thematic groupings).
    Returns dict mapping theme → Scenario object.
    """
    logger.info("Seeding scenarios...")
    scenario_map = {}

    for scenario_data in SEED_SCENARIOS:
        # Check if scenario already exists
        existing = db.query(Scenario).filter(Scenario.title == scenario_data["title"]).first()
        if existing:
            logger.debug(f"Scenario '{scenario_data['title']}' already exists, skipping")
            scenario_map[scenario_data["theme"]] = existing
            continue

        # Create scenario
        scenario = Scenario(
            title=scenario_data["title"],
            description=scenario_data["description"],
            theme=scenario_data["theme"],
            context=scenario_data.get("context"),
            recommended_level=scenario_data.get("recommended_level")
        )
        db.add(scenario)
        scenario_map[scenario_data["theme"]] = scenario
        logger.debug(f"Added scenario: {scenario_data['title']}")

    db.commit()
    logger.info(f"✅ Seeded {len(scenario_map)} scenarios")
    return scenario_map


def link_exercises_to_scenarios(db: Session, exercises: list, scenario_map: dict):
    """
    Link exercises to scenarios based on trigger phrases and themes.
    """
    logger.info("Linking exercises to scenarios...")

    # Define mappings: trigger_phrase → scenario theme
    trigger_to_scenario = {
        # Emotional reactions
        "espero que": "emotions",
        "me alegra que": "emotional_reactions",
        "me sorprende que": "emotional_reactions",
        "temo que": "emotional_reactions",
        "me molesta que": "emotional_reactions",
        "me preocupa que": "relationships",
        "me gusta que": "emotions",
        "ojalá que": "emotions",
        "ojalá": "emotions",

        # Doubt and uncertainty
        "dudo que": "doubt",
        "no creo que": "doubt",
        "no pienso que": "doubt",
        "no es cierto que": "doubt",
        "no es verdad que": "doubt",
        "es imposible que": "doubt",
        "es posible que": "doubt",

        # Wishes and requests
        "quiero que": "relationships",
        "prefiero que": "advice",
        "sugiero que": "advice",
        "recomiendo que": "advice",
        "pido que": "work",
        "necesito que": "work",
        "deseo que": "emotions",

        # Impersonal expressions
        "es importante que": "advice",
        "es necesario que": "advice",
        "es mejor que": "advice",
        "es bueno que": "health",
        "es malo que": "health",
        "es raro que": "doubt",

        # Conjunctions
        "cuando": "future_plans",
        "aunque": "hypothetical",
        "para que": "hypothetical",
        "sin que": "hypothetical",
        "antes de que": "future_plans",
        "hasta que": "future_plans",
        "en cuanto": "future_plans",
        "a menos que": "hypothetical",
        "si": "hypothetical",
    }

    links_created = 0
    for exercise in exercises:
        trigger = exercise.trigger_phrase
        if not trigger:
            continue

        # Find matching scenario
        scenario_theme = trigger_to_scenario.get(trigger)
        if not scenario_theme or scenario_theme not in scenario_map:
            logger.debug(f"No scenario mapping for trigger: {trigger}")
            continue

        scenario = scenario_map[scenario_theme]

        # Check if link already exists
        existing_link = db.query(ExerciseScenario).filter(
            ExerciseScenario.exercise_id == exercise.id,
            ExerciseScenario.scenario_id == scenario.id
        ).first()

        if existing_link:
            continue

        # Create link
        link = ExerciseScenario(
            exercise_id=exercise.id,
            scenario_id=scenario.id,
            order_index=0  # Could be improved with proper ordering
        )
        db.add(link)
        links_created += 1

    db.commit()
    logger.info(f"✅ Created {links_created} exercise-scenario links")


def main():
    """
    Main seeding function.
    """
    logger.info("="*70)
    logger.info("Starting database seeding...")
    logger.info("="*70)

    # Create tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables ready")

    # Get database session
    db = SessionLocal()

    try:
        # Seed data in order (respecting foreign key dependencies)
        verb_map = seed_verbs(db)
        exercises = seed_exercises(db, verb_map)
        scenario_map = seed_scenarios(db)
        link_exercises_to_scenarios(db, exercises, scenario_map)

        # Summary
        logger.info("="*70)
        logger.info("🎉 SEEDING COMPLETE!")
        logger.info("="*70)
        logger.info(f"📚 Verbs: {len(verb_map)}")
        logger.info(f"✏️  Exercises: {len(exercises)}")
        logger.info(f"🎯 Scenarios: {len(scenario_map)}")
        logger.info("="*70)

        # Difficulty breakdown
        difficulty_counts = {}
        for exercise in exercises:
            diff = exercise.difficulty.name
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1

        logger.info("Exercise Difficulty Breakdown:")
        for diff, count in sorted(difficulty_counts.items()):
            logger.info(f"  {diff}: {count} exercises")

        logger.info("="*70)
        logger.info("✅ Database is ready for testing!")
        logger.info("="*70)

    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
