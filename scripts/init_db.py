#!/usr/bin/env python3
"""
Database initialization script.
Creates all tables and optionally seeds with initial data.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path.parent))

from backend.core.database import engine, Base, get_db, init_db, reset_db
from backend.models import Verb, Achievement
from backend.core.seed_data import SEED_VERBS, SEED_ACHIEVEMENTS


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    init_db()
    print("✓ Tables created successfully")


def seed_verbs():
    """Seed database with common Spanish verbs."""
    print("\nSeeding verbs...")

    with get_db() as db:
        # Check if verbs already exist
        existing_count = db.query(Verb).count()
        if existing_count > 0:
            print(f"  Found {existing_count} existing verbs, skipping seed")
            return

        # Add all seed verbs
        for verb_data in SEED_VERBS:
            verb = Verb(**verb_data)
            db.add(verb)

        db.commit()
        print(f"✓ Seeded {len(SEED_VERBS)} verbs")


def seed_achievements():
    """Seed database with achievements."""
    print("\nSeeding achievements...")

    with get_db() as db:
        # Check if achievements already exist
        existing_count = db.query(Achievement).count()
        if existing_count > 0:
            print(f"  Found {existing_count} existing achievements, skipping seed")
            return

        # Add all seed achievements
        for achievement_data in SEED_ACHIEVEMENTS:
            achievement = Achievement(**achievement_data)
            db.add(achievement)

        db.commit()
        print(f"✓ Seeded {len(SEED_ACHIEVEMENTS)} achievements")


def main():
    """Main initialization function."""
    import argparse

    parser = argparse.ArgumentParser(description="Initialize the database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop all tables before creating (WARNING: Destroys all data!)"
    )
    parser.add_argument(
        "--no-seed",
        action="store_true",
        help="Skip seeding data"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("Spanish Subjunctive Practice - Database Setup")
    print("=" * 50)

    if args.reset:
        response = input("\n⚠️  WARNING: This will delete ALL data. Continue? (yes/no): ")
        if response.lower() != "yes":
            print("Aborted.")
            return
        print("\nResetting database...")
        reset_db()
        print("✓ Database reset complete")
    else:
        create_tables()

    if not args.no_seed:
        seed_verbs()
        seed_achievements()

    print("\n" + "=" * 50)
    print("✓ Database initialization complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
