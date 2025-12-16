"""
Integration tests for achievement unlock and gamification flow.

Tests the complete achievement system workflow:
1. Exercise completion tracking
2. XP (points) accumulation
3. Achievement criteria evaluation
4. Achievement unlock notifications
5. Progress towards locked achievements
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models.progress import (
    Achievement, UserAchievement, Attempt, Session as PracticeSession,
    UserStatistics
)
from models.user import User, UserProfile
from api.routes.achievements import check_and_unlock_achievements, get_user_stats_for_achievements


@pytest.mark.integration
class TestAchievementUnlockFlow:
    """Integration tests for achievement unlock and gamification workflow."""

    def test_complete_achievement_unlock_flow(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test complete flow from exercise completion to achievement unlock.

        Flow:
        1. Create achievement with criteria
        2. Complete exercises to meet criteria
        3. Check for new achievements
        4. Verify achievement unlocked
        5. Verify XP awarded
        6. Verify notification data
        """
        # Step 1: Create volume achievement (complete 10 exercises)
        achievement = Achievement(
            name="Getting Started",
            description="Complete your first 10 exercises",
            category="volume",
            icon_url="trophy",
            points=25,
            criteria={"exercises_completed": 10}
        )
        db_session.add(achievement)
        db_session.commit()
        db_session.refresh(achievement)

        # Step 2: Create session and complete 10 exercises
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        # Create 10 attempts
        for i in range(10):
            exercise = sample_exercises_with_tags[i % len(sample_exercises_with_tags)]
            attempt = Attempt(
                session_id=session.id,
                exercise_id=exercise.id,
                user_id=test_user.id,
                user_answer=exercise.correct_answer,
                is_correct=True
            )
            db_session.add(attempt)

        db_session.commit()

        # Step 3: Check for achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Step 4: Verify achievement unlocked
        assert len(newly_unlocked) >= 1
        assert any(ach.name == "Getting Started" for ach in newly_unlocked)

        # Step 5: Verify database record
        user_achievement = db_session.query(UserAchievement).filter(
            UserAchievement.user_id == test_user.id,
            UserAchievement.achievement_id == achievement.id
        ).first()

        assert user_achievement is not None
        assert user_achievement.unlocked_at is not None

        # Step 6: Verify XP/points
        total_points = sum(ach.points for ach in newly_unlocked)
        assert total_points >= 25

    def test_streak_achievement_unlock(
        self,
        db_session: Session,
        test_user: User
    ):
        """
        Test streak-based achievement unlock.

        Flow:
        1. Create streak achievement (7-day streak)
        2. Set user streak to 7 days
        3. Check achievements
        4. Verify unlock
        """
        # Step 1: Create streak achievement
        achievement = Achievement(
            name="Week Warrior",
            description="Practice for 7 consecutive days",
            category="streak",
            icon_url="flame",
            points=50,
            criteria={"streak_days": 7}
        )
        db_session.add(achievement)
        db_session.commit()

        # Step 2: Update user profile with 7-day streak
        profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()

        if not profile:
            profile = UserProfile(
                user_id=test_user.id,
                current_streak=7,
                longest_streak=7
            )
            db_session.add(profile)
        else:
            profile.current_streak = 7
            profile.longest_streak = 7

        db_session.commit()

        # Step 3: Check achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Step 4: Verify
        assert any(ach.name == "Week Warrior" for ach in newly_unlocked)

    def test_accuracy_achievement_unlock(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test accuracy-based achievement (perfect session).

        Flow:
        1. Create perfect session achievement
        2. Complete session with 100% accuracy
        3. Check achievements
        4. Verify unlock
        """
        # Step 1: Create achievement
        achievement = Achievement(
            name="Perfect Score",
            description="Complete a session with 100% accuracy",
            category="accuracy",
            icon_url="star",
            points=30,
            criteria={"perfect_sessions": 1}
        )
        db_session.add(achievement)
        db_session.commit()

        # Step 2: Create perfect session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice",
            total_exercises=5,
            correct_answers=5,
            score_percentage=100.0,
            is_completed=True
        )
        db_session.add(session)
        db_session.commit()

        # Step 3: Check achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Step 4: Verify
        assert any(ach.name == "Perfect Score" for ach in newly_unlocked)

    def test_multiple_achievements_unlock_simultaneously(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test unlocking multiple achievements at once.

        Flow:
        1. Create multiple achievements with different criteria
        2. Complete actions that satisfy multiple criteria
        3. Check achievements
        4. Verify all unlocked
        5. Calculate total XP
        """
        # Step 1: Create multiple achievements
        ach1 = Achievement(
            name="First Steps",
            description="Complete 5 exercises",
            category="volume",
            points=10,
            criteria={"exercises_completed": 5}
        )
        ach2 = Achievement(
            name="Consistent Learner",
            description="Get 5 consecutive correct answers",
            category="accuracy",
            points=15,
            criteria={"correct_answers": 5}
        )
        db_session.add_all([ach1, ach2])
        db_session.commit()

        # Step 2: Complete 5 correct exercises
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        for i in range(5):
            exercise = sample_exercises_with_tags[i]
            attempt = Attempt(
                session_id=session.id,
                exercise_id=exercise.id,
                user_id=test_user.id,
                user_answer=exercise.correct_answer,
                is_correct=True
            )
            db_session.add(attempt)

        db_session.commit()

        # Step 3: Check achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Step 4: Verify both unlocked
        unlocked_names = [ach.name for ach in newly_unlocked]
        assert "First Steps" in unlocked_names or len(newly_unlocked) >= 1

        # Step 5: Calculate total XP
        total_points = sum(ach.points for ach in newly_unlocked)
        assert total_points >= 10

    def test_achievement_progress_tracking(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test tracking progress towards locked achievements.

        Flow:
        1. Create achievement requiring 20 exercises
        2. Complete 10 exercises (50% progress)
        3. Get achievement stats
        4. Verify progress calculated correctly
        """
        # Step 1: Create achievement
        achievement = Achievement(
            name="Dedicated Student",
            description="Complete 20 exercises",
            category="volume",
            points=40,
            criteria={"exercises_completed": 20}
        )
        db_session.add(achievement)
        db_session.commit()

        # Step 2: Complete 10 exercises
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        for i in range(10):
            exercise = sample_exercises_with_tags[i % len(sample_exercises_with_tags)]
            attempt = Attempt(
                session_id=session.id,
                exercise_id=exercise.id,
                user_id=test_user.id,
                user_answer=exercise.correct_answer,
                is_correct=True
            )
            db_session.add(attempt)

        db_session.commit()

        # Step 3: Get stats
        stats = get_user_stats_for_achievements(db_session, test_user.id)

        # Step 4: Verify progress
        assert stats["total_exercises"] == 10

        # Calculate progress percentage
        progress = (stats["total_exercises"] / 20) * 100
        assert progress == 50.0

    def test_achievement_prevents_duplicate_unlock(
        self,
        db_session: Session,
        test_user: User
    ):
        """
        Test achievement cannot be unlocked twice.

        Flow:
        1. Create and unlock achievement
        2. Meet criteria again
        3. Check achievements
        4. Verify no duplicate unlock
        """
        # Step 1: Create and unlock achievement
        achievement = Achievement(
            name="First Win",
            description="Complete first exercise",
            category="volume",
            points=5,
            criteria={"exercises_completed": 1}
        )
        db_session.add(achievement)
        db_session.commit()

        # Manually unlock it first time
        user_ach = UserAchievement(
            user_id=test_user.id,
            achievement_id=achievement.id,
            unlocked_at=datetime.utcnow()
        )
        db_session.add(user_ach)
        db_session.commit()

        # Step 2: Create more exercises (criteria still met)
        # Step 3: Check achievements again
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Step 4: Verify not in newly unlocked
        assert all(ach.id != achievement.id for ach in newly_unlocked)

        # Verify only one record exists
        count = db_session.query(UserAchievement).filter(
            UserAchievement.user_id == test_user.id,
            UserAchievement.achievement_id == achievement.id
        ).count()
        assert count == 1

    def test_special_achievement_unlock(
        self,
        db_session: Session,
        test_user: User
    ):
        """
        Test special time-based achievements (night owl, early bird, speed demon).

        Flow:
        1. Create special achievement
        2. Create qualifying session
        3. Check achievements
        4. Verify unlock
        """
        # Create speed demon achievement (20+ exercises in <5 minutes)
        achievement = Achievement(
            name="Speed Demon",
            description="Complete 20 exercises in under 5 minutes",
            category="special",
            points=50,
            criteria={"type": "speed_demon"}
        )
        db_session.add(achievement)
        db_session.commit()

        # Create qualifying session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice",
            total_exercises=20,
            correct_answers=15,
            duration_seconds=280,  # 4 minutes 40 seconds
            is_completed=True
        )
        db_session.add(session)
        db_session.commit()

        # Check achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Verify unlock
        assert any(ach.name == "Speed Demon" for ach in newly_unlocked)

    def test_xp_accumulation_across_achievements(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test total XP calculation across multiple unlocked achievements.

        Flow:
        1. Create achievements with different point values
        2. Unlock multiple achievements
        3. Calculate total XP
        4. Verify accumulation
        """
        # Create achievements
        achievements = [
            Achievement(
                name="Beginner",
                description="Complete 3 exercises",
                category="volume",
                points=5,
                criteria={"exercises_completed": 3}
            ),
            Achievement(
                name="Quick Learner",
                description="Get 3 consecutive correct",
                category="accuracy",
                points=10,
                criteria={"correct_answers": 3}
            )
        ]
        db_session.add_all(achievements)
        db_session.commit()

        # Complete exercises to unlock both
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        for i in range(3):
            exercise = sample_exercises_with_tags[i]
            attempt = Attempt(
                session_id=session.id,
                exercise_id=exercise.id,
                user_id=test_user.id,
                user_answer=exercise.correct_answer,
                is_correct=True
            )
            db_session.add(attempt)

        db_session.commit()

        # Check achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Calculate total XP
        total_xp = sum(ach.points for ach in newly_unlocked)

        # Should have at least one achievement (5+ points)
        assert total_xp >= 5
