#!/usr/bin/env python3
"""
Test Data Creation Script

Creates test users with different levels of progress for user testing.
Run this after initializing the database to populate with realistic test data.

Usage:
    python scripts/create_test_data.py
    python scripts/create_test_data.py --reset  # Reset and recreate all test data
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Import models
from backend.models.user import User
from backend.models.exercise import Exercise, ExerciseType, DifficultyLevel, UserAnswer
from backend.models.progress import Progress, Achievement
from backend.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)


# Test user configurations
TEST_USERS = [
    {
        "email": "new@test.com",
        "password": "TestPass123!",
        "username": "New User",
        "description": "Brand new user with no progress",
        "level": 1,
        "xp": 0,
        "exercises_completed": 0,
        "streak": 0,
    },
    {
        "email": "beginner@test.com",
        "password": "TestPass123!",
        "username": "Beginner User",
        "description": "Beginner with 1-2 sessions completed",
        "level": 2,
        "xp": 250,
        "exercises_completed": 10,
        "streak": 2,
    },
    {
        "email": "active@test.com",
        "password": "TestPass123!",
        "username": "Active User",
        "description": "Active user with regular practice",
        "level": 5,
        "xp": 1200,
        "exercises_completed": 50,
        "streak": 7,
    },
    {
        "email": "advanced@test.com",
        "password": "TestPass123!",
        "username": "Advanced User",
        "description": "Advanced user with high level and achievements",
        "level": 10,
        "xp": 5000,
        "exercises_completed": 200,
        "streak": 30,
    },
]


async def create_test_users(session: AsyncSession):
    """Create test users with varying levels of progress."""

    print("\n🧑 Creating test users...")

    for user_data in TEST_USERS:
        # Check if user already exists
        existing = await session.execute(
            "SELECT * FROM users WHERE email = :email",
            {"email": user_data["email"]}
        )
        if existing.first():
            print(f"  ⚠️  User {user_data['email']} already exists, skipping...")
            continue

        # Create user
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            hashed_password=hash_password(user_data["password"]),
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=user_data["streak"]),
        )

        session.add(user)
        await session.flush()  # Get user ID

        # Create progress record
        progress = Progress(
            user_id=user.id,
            level=user_data["level"],
            total_xp=user_data["xp"],
            exercises_completed=user_data["exercises_completed"],
            current_streak=user_data["streak"],
            longest_streak=user_data["streak"],
            total_practice_time_minutes=user_data["exercises_completed"] * 3,  # ~3 min per exercise
        )

        session.add(progress)

        print(f"  ✓ Created {user_data['email']} - Level {user_data['level']}, {user_data['xp']} XP")

    await session.commit()
    print("✓ Test users created successfully!\n")


async def create_sample_exercises(session: AsyncSession):
    """Create a set of sample exercises for testing."""

    print("📝 Creating sample exercises...")

    sample_exercises = [
        # Easy - Fill in blank
        {
            "type": ExerciseType.FILL_IN_BLANK,
            "difficulty": DifficultyLevel.EASY,
            "spanish_text": "Espero que tú ____ (estar) bien.",
            "correct_answer": "estés",
            "hint": "Present subjunctive of 'estar' for 'tú'",
            "explanation": "After 'espero que' we use the present subjunctive. The verb 'estar' for 'tú' becomes 'estés'.",
            "trigger": "espero que",
        },
        {
            "type": ExerciseType.CONJUGATION,
            "difficulty": DifficultyLevel.EASY,
            "spanish_text": "Es importante que nosotros ____ (hablar) español.",
            "correct_answer": "hablemos",
            "hint": "Present subjunctive of 'hablar' for 'nosotros'",
            "explanation": "'Es importante que' triggers the subjunctive. For -ar verbs, take the yo form, drop -o, add -emos for nosotros.",
            "trigger": "es importante que",
        },
        # Medium exercises
        {
            "type": ExerciseType.TRANSLATION,
            "difficulty": DifficultyLevel.MEDIUM,
            "english_text": "I want you to study.",
            "correct_answer": "Quiero que estudies.",
            "hint": "Use 'querer que' + subjunctive",
            "explanation": "'Querer que' expresses desire and requires subjunctive in Spanish.",
            "trigger": "quiero que",
        },
        {
            "type": ExerciseType.TRIGGER_IDENTIFICATION,
            "difficulty": DifficultyLevel.MEDIUM,
            "spanish_text": "Dudo que él venga a la fiesta.",
            "correct_answer": "dudo que",
            "hint": "Look for expressions of doubt",
            "explanation": "'Dudo que' expresses doubt/uncertainty, which always triggers subjunctive mood.",
            "trigger": "dudo que",
        },
        # Hard exercises
        {
            "type": ExerciseType.FILL_IN_BLANK,
            "difficulty": DifficultyLevel.HARD,
            "spanish_text": "Si yo ____ (ser) rico, viajaría por el mundo.",
            "correct_answer": "fuera",
            "hint": "Imperfect subjunctive for hypothetical situations",
            "explanation": "In 'si' clauses for hypothetical/contrary-to-fact situations, use imperfect subjunctive.",
            "trigger": "si (hypothetical)",
        },
        {
            "type": ExerciseType.CONJUGATION,
            "difficulty": DifficultyLevel.HARD,
            "spanish_text": "Aunque ____ (llover), iré a correr.",
            "correct_answer": "llueva",
            "hint": "Present subjunctive with 'aunque' (hypothetical)",
            "explanation": "'Aunque' with subjunctive expresses a hypothetical situation. 'Llover' is an irregular stem-changing verb.",
            "trigger": "aunque",
        },
        # Very Hard exercises
        {
            "type": ExerciseType.TRANSLATION,
            "difficulty": DifficultyLevel.VERY_HARD,
            "english_text": "I would have wanted them to have arrived earlier.",
            "correct_answer": "Habría querido que hubieran llegado más temprano.",
            "hint": "Conditional perfect + pluperfect subjunctive",
            "explanation": "This requires conditional perfect (habría querido) + past perfect subjunctive (hubieran llegado) for a hypothetical past situation.",
            "trigger": "conditional + past subjunctive",
        },
        {
            "type": ExerciseType.FILL_IN_BLANK,
            "difficulty": DifficultyLevel.EXPERT,
            "spanish_text": "No había nadie que ____ (poder) resolver el problema.",
            "correct_answer": "pudiera",
            "hint": "Imperfect subjunctive in past negative existential",
            "explanation": "With negative existential statements in the past, use imperfect subjunctive. 'Poder' becomes 'pudiera/pudiese'.",
            "trigger": "no había nadie que",
        },
    ]

    for ex in sample_exercises:
        # Check if similar exercise exists
        existing = await session.execute(
            "SELECT COUNT(*) FROM exercises WHERE spanish_text = :text",
            {"text": ex.get("spanish_text", "")}
        )
        if existing.scalar() > 0:
            continue

        exercise = Exercise(
            type=ex["type"],
            difficulty=ex["difficulty"],
            spanish_text=ex.get("spanish_text"),
            english_text=ex.get("english_text"),
            correct_answer=ex["correct_answer"],
            hint=ex.get("hint"),
            explanation=ex["explanation"],
            trigger=ex.get("trigger"),
        )

        session.add(exercise)

    await session.commit()
    print(f"✓ Sample exercises created!\n")


async def create_practice_history(session: AsyncSession):
    """Create practice history for test users (except new user)."""

    print("📊 Creating practice history...")

    # Get users
    result = await session.execute("SELECT * FROM users WHERE email != 'new@test.com'")
    users = result.fetchall()

    # Get exercises
    result = await session.execute("SELECT * FROM exercises LIMIT 20")
    exercises = result.fetchall()

    if not exercises:
        print("  ⚠️  No exercises found. Run create_sample_exercises first.")
        return

    for user_row in users:
        user_email = user_row[1]  # Assuming email is column 1
        user_id = user_row[0]  # Assuming id is column 0

        # Get user data
        user_data = next((u for u in TEST_USERS if u["email"] == user_email), None)
        if not user_data:
            continue

        exercises_to_create = user_data["exercises_completed"]

        # Create answers for this user
        for i in range(exercises_to_create):
            exercise = exercises[i % len(exercises)]

            # Simulate varying accuracy (80% correct on average)
            is_correct = i % 5 != 0  # 80% correct

            answer = UserAnswer(
                user_id=user_id,
                exercise_id=exercise[0],  # exercise id
                user_answer=exercise[4] if is_correct else "wrong answer",  # correct_answer is column 4
                is_correct=is_correct,
                time_taken_seconds=30 + (i % 60),  # 30-90 seconds
                submitted_at=datetime.utcnow() - timedelta(days=exercises_to_create - i),
            )

            session.add(answer)

        print(f"  ✓ Created {exercises_to_create} practice answers for {user_email}")

    await session.commit()
    print("✓ Practice history created!\n")


async def create_achievements(session: AsyncSession):
    """Create achievement definitions."""

    print("🏆 Creating achievements...")

    achievements = [
        {
            "name": "First Steps",
            "description": "Complete your first exercise",
            "icon": "🎯",
            "criteria": "exercises_completed >= 1",
            "points": 10,
        },
        {
            "name": "Getting Started",
            "description": "Complete 10 exercises",
            "icon": "📚",
            "criteria": "exercises_completed >= 10",
            "points": 50,
        },
        {
            "name": "Dedicated Learner",
            "description": "Complete 50 exercises",
            "icon": "⭐",
            "criteria": "exercises_completed >= 50",
            "points": 100,
        },
        {
            "name": "Subjunctive Master",
            "description": "Complete 100 exercises",
            "icon": "👑",
            "criteria": "exercises_completed >= 100",
            "points": 200,
        },
        {
            "name": "Week Warrior",
            "description": "Practice 7 days in a row",
            "icon": "🔥",
            "criteria": "current_streak >= 7",
            "points": 75,
        },
        {
            "name": "Month Master",
            "description": "Practice 30 days in a row",
            "icon": "💪",
            "criteria": "current_streak >= 30",
            "points": 300,
        },
        {
            "name": "Accuracy Ace",
            "description": "Achieve 90% accuracy over 20 exercises",
            "icon": "🎓",
            "criteria": "accuracy >= 90 AND exercises_completed >= 20",
            "points": 150,
        },
        {
            "name": "Level Up",
            "description": "Reach level 5",
            "icon": "🚀",
            "criteria": "level >= 5",
            "points": 100,
        },
        {
            "name": "Expert Level",
            "description": "Reach level 10",
            "icon": "💎",
            "criteria": "level >= 10",
            "points": 250,
        },
    ]

    for ach in achievements:
        # Check if exists
        existing = await session.execute(
            "SELECT COUNT(*) FROM achievements WHERE name = :name",
            {"name": ach["name"]}
        )
        if existing.scalar() > 0:
            continue

        achievement = Achievement(
            name=ach["name"],
            description=ach["description"],
            icon=ach["icon"],
            criteria=ach["criteria"],
            points=ach["points"],
        )

        session.add(achievement)

    await session.commit()
    print(f"✓ Achievements created!\n")


async def main():
    """Main function to create all test data."""

    print("\n" + "="*60)
    print("🧪 TEST DATA CREATION SCRIPT")
    print("="*60)
    print("\nThis script will create test users and sample data.")
    print("Test accounts will have password: [REDACTED] (see script source for password)\n")

    # Check for reset flag
    reset = "--reset" in sys.argv
    if reset:
        print("⚠️  RESET MODE: Will delete existing test data first\n")
        response = input("Are you sure? This will delete test users! (yes/no): ")
        if response.lower() != "yes":
            print("Cancelled.")
            return

    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        if "postgresql" in settings.DATABASE_URL
        else settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"),
        echo=False,
    )

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        try:
            if reset:
                print("🗑️  Deleting existing test data...")
                await session.execute(
                    "DELETE FROM users WHERE email LIKE '%@test.com'"
                )
                await session.commit()
                print("✓ Test data cleared\n")

            # Create all test data
            await create_test_users(session)
            await create_sample_exercises(session)
            await create_practice_history(session)
            await create_achievements(session)

            print("\n" + "="*60)
            print("✅ TEST DATA CREATED SUCCESSFULLY!")
            print("="*60)
            print("\n📋 Test Accounts Created:\n")

            for user in TEST_USERS:
                print(f"  Email: {user['email']}")
                print(f"  Password: [REDACTED]")
                print(f"  Level: {user['level']} | XP: {user['xp']} | Exercises: {user['exercises_completed']}")
                print(f"  Description: {user['description']}")
                print()

            print("ℹ️  Note: All test accounts use the same password.")
            print("   Check the TEST_USERS configuration in this script for the password.")

            print("🚀 You can now use these accounts for user testing!")
            print("\nNext steps:")
            print("  1. Start backend: uvicorn main:app --reload")
            print("  2. Start frontend: npm run dev")
            print("  3. Login with any test account")
            print("  4. Begin user testing scenarios")
            print()

        except Exception as e:
            print(f"\n❌ Error creating test data: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
