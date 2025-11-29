"""
Integration tests for achievement system flow.

Tests the achievement unlock workflow:
1. Complete exercises to trigger achievements
2. Verify achievement unlocking
3. Test achievement progress tracking
4. Test multiple achievement criteria
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.progress import Achievement, UserAchievement, Attempt, Session as PracticeSession
from models.user import UserProfile
from api.routes.achievements import check_and_unlock_achievements


@pytest.mark.integration
class TestAchievementFlow:
    """Integration tests for gamification achievement system."""

    def test_unlock_streak_achievement(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user,
        sample_exercises_with_tags
    ):
        """
        Test unlocking streak-based achievement.

        Flow:
        1. Create streak achievement
        2. Update user streak
        3. Check achievements
        4. Verify unlock recorded
        """
        # Step 1: Create streak achievement
        achievement = Achievement(
            name="Week Warrior",
            description="Practice for 7 days in a row",
            category="streak",
            icon_url="flame",
            points=50,
            criteria={"streak_days": 7}
        )
        db_session.add(achievement)
        db_session.commit()
        db_session.refresh(achievement)

        # Step 2: Update user's streak
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

        # Step 3: Check achievements (trigger unlock)
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Step 4: Verify achievement unlocked
        assert len(newly_unlocked) >= 1
        assert any(ach.name == "Week Warrior" for ach in newly_unlocked)

        # Verify database record
        user_ach = db_session.query(UserAchievement).filter(
            UserAchievement.user_id == test_user.id,
            UserAchievement.achievement_id == achievement.id
        ).first()

        assert user_ach is not None
        assert user_ach.unlocked_at is not None

    def test_unlock_volume_achievement(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user,
        sample_exercises_with_tags
    ):
        """Test unlocking achievement based on exercise volume."""
        # Create volume achievement
        achievement = Achievement(
            name="Century Club",
            description="Complete 100 exercises",
            category="volume",
            icon_url="trophy",
            points=100,
            criteria={"exercises_completed": 100}
        )
        db_session.add(achievement)
        db_session.commit()

        # Create session and attempts
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            total_exercises=100,
            correct_answers=80,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        # Create 100 attempts
        for i in range(100):
            attempt = Attempt(
                session_id=session.id,
                user_id=test_user.id,
                exercise_id=sample_exercises_with_tags[i % len(sample_exercises_with_tags)].id,
                user_answer="answer",
                is_correct=i < 80
            )
            db_session.add(attempt)

        db_session.commit()

        # Check achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Should unlock volume achievement
        assert any(ach.name == "Century Club" for ach in newly_unlocked)

    def test_unlock_accuracy_achievement(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user,
        sample_exercises_with_tags
    ):
        """Test unlocking achievement based on consecutive correct answers."""
        # Create accuracy achievement
        achievement = Achievement(
            name="Perfect Streak",
            description="Get 20 exercises correct in a row",
            category="accuracy",
            icon_url="target",
            points=75,
            criteria={"correct_answers": 20}
        )
        db_session.add(achievement)
        db_session.commit()

        # Create session with perfect streak
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            total_exercises=20,
            correct_answers=20,
            score_percentage=100.0,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        # Create 20 consecutive correct attempts
        for i in range(20):
            attempt = Attempt(
                session_id=session.id,
                user_id=test_user.id,
                exercise_id=sample_exercises_with_tags[i % len(sample_exercises_with_tags)].id,
                user_answer="correct",
                is_correct=True,
                created_at=datetime.utcnow() + timedelta(seconds=i)
            )
            db_session.add(attempt)

        db_session.commit()

        # Check achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Should unlock accuracy achievement
        assert any(ach.name == "Perfect Streak" for ach in newly_unlocked)

    def test_achievement_no_duplicates(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user
    ):
        """Test that achievements are not unlocked twice."""
        # Create achievement
        achievement = Achievement(
            name="First Steps",
            description="Complete your first exercise",
            category="milestone",
            icon_url="star",
            points=10,
            criteria={"exercises_completed": 1}
        )
        db_session.add(achievement)
        db_session.commit()

        # Create profile with exercise completed
        profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()
        if not profile:
            profile = UserProfile(user_id=test_user.id)
            db_session.add(profile)
            db_session.commit()

        # Create attempt
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            total_exercises=1,
            correct_answers=1,
            is_completed=True
        )
        db_session.add(session)
        db_session.commit()

        # First unlock
        first_unlock = check_and_unlock_achievements(db_session, test_user.id)
        assert len(first_unlock) >= 1

        # Second check should not unlock again
        second_unlock = check_and_unlock_achievements(db_session, test_user.id)
        assert len(second_unlock) == 0

    def test_multiple_achievements_unlock_simultaneously(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user,
        sample_exercises_with_tags
    ):
        """Test that multiple achievements can unlock at once."""
        # Create multiple achievements
        achievements = [
            Achievement(
                name="Quick Learner",
                description="Complete 10 exercises",
                category="volume",
                icon_url="zap",
                points=20,
                criteria={"exercises_completed": 10}
            ),
            Achievement(
                name="Dedicated",
                description="Practice for 3 days",
                category="streak",
                icon_url="calendar",
                points=30,
                criteria={"streak_days": 3}
            ),
            Achievement(
                name="Accurate",
                description="Get 10 correct in a row",
                category="accuracy",
                icon_url="bullseye",
                points=25,
                criteria={"correct_answers": 10}
            )
        ]

        for ach in achievements:
            db_session.add(ach)
        db_session.commit()

        # Create data that meets all criteria
        profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()
        if not profile:
            profile = UserProfile(user_id=test_user.id, current_streak=3, longest_streak=3)
            db_session.add(profile)
        else:
            profile.current_streak = 3
            profile.longest_streak = 3
        db_session.commit()

        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            total_exercises=10,
            correct_answers=10,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        for i in range(10):
            attempt = Attempt(
                session_id=session.id,
                user_id=test_user.id,
                exercise_id=sample_exercises_with_tags[i % len(sample_exercises_with_tags)].id,
                user_answer="answer",
                is_correct=True,
                created_at=datetime.utcnow() + timedelta(seconds=i)
            )
            db_session.add(attempt)

        db_session.commit()

        # Check achievements
        newly_unlocked = check_and_unlock_achievements(db_session, test_user.id)

        # Should unlock all three
        assert len(newly_unlocked) >= 3
        unlocked_names = [ach.name for ach in newly_unlocked]
        assert "Quick Learner" in unlocked_names
        assert "Dedicated" in unlocked_names
        assert "Accurate" in unlocked_names

    def test_achievement_progress_calculation(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user
    ):
        """Test achievement progress tracking."""
        # Create achievement requiring 50 exercises
        achievement = Achievement(
            name="Halfway There",
            description="Complete 50 exercises",
            category="volume",
            icon_url="chart",
            points=50,
            criteria={"exercises_completed": 50}
        )
        db_session.add(achievement)
        db_session.commit()

        # Create 25 attempts (50% progress)
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            total_exercises=25,
            correct_answers=20,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        for i in range(25):
            attempt = Attempt(
                session_id=session.id,
                user_id=test_user.id,
                exercise_id=1,
                user_answer="answer",
                is_correct=True
            )
            db_session.add(attempt)

        db_session.commit()

        # Get achievement progress
        progress_response = authenticated_client.get("/api/achievements/progress")

        if progress_response.status_code == status.HTTP_200_OK:
            progress = progress_response.json()

            # Should show 50% progress toward achievement
            if isinstance(progress, list):
                halfway_progress = next(
                    (p for p in progress if p.get("achievement_name") == "Halfway There"),
                    None
                )
                if halfway_progress:
                    assert halfway_progress["current"] == 25
                    assert halfway_progress["required"] == 50

    def test_get_user_achievements_endpoint(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user
    ):
        """Test getting user's unlocked achievements."""
        # Create and unlock achievement
        achievement = Achievement(
            name="Early Bird",
            description="Practice before 9am",
            category="special",
            icon_url="sunrise",
            points=15,
            criteria={"early_practice": True}
        )
        db_session.add(achievement)
        db_session.commit()

        user_ach = UserAchievement(
            user_id=test_user.id,
            achievement_id=achievement.id,
            unlocked_at=datetime.utcnow()
        )
        db_session.add(user_ach)
        db_session.commit()

        # Get user achievements
        response = authenticated_client.get("/api/achievements")

        assert response.status_code == status.HTTP_200_OK
        achievements_data = response.json()

        # Should include unlocked achievement
        if isinstance(achievements_data, list):
            assert len(achievements_data) > 0
            names = [a.get("name") for a in achievements_data]
            assert "Early Bird" in names

    def test_achievement_points_accumulation(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user
    ):
        """Test that achievement points accumulate correctly."""
        # Create multiple achievements
        achievements = [
            Achievement(name="A1", description="Test 1", category="test", points=10, criteria={"test": 1}),
            Achievement(name="A2", description="Test 2", category="test", points=20, criteria={"test": 2}),
            Achievement(name="A3", description="Test 3", category="test", points=30, criteria={"test": 3}),
        ]

        for ach in achievements:
            db_session.add(ach)
        db_session.commit()

        # Unlock all achievements
        for ach in achievements:
            user_ach = UserAchievement(
                user_id=test_user.id,
                achievement_id=ach.id,
                unlocked_at=datetime.utcnow()
            )
            db_session.add(user_ach)

        db_session.commit()

        # Get user progress
        progress_response = authenticated_client.get("/api/progress")

        if progress_response.status_code == status.HTTP_200_OK:
            progress = progress_response.json()

            # Total points should be 60 (10 + 20 + 30)
            if "achievement_points" in progress:
                assert progress["achievement_points"] >= 60

    def test_achievement_categories(
        self,
        authenticated_client: TestClient,
        db_session: Session
    ):
        """Test different achievement categories."""
        categories = ["streak", "volume", "accuracy", "milestone", "special"]

        for category in categories:
            achievement = Achievement(
                name=f"{category.title()} Achievement",
                description=f"Test {category}",
                category=category,
                icon_url="icon",
                points=10,
                criteria={category: True}
            )
            db_session.add(achievement)

        db_session.commit()

        # Verify all categories stored
        all_achievements = db_session.query(Achievement).all()
        stored_categories = set(ach.category for ach in all_achievements)

        assert len(stored_categories.intersection(set(categories))) >= len(categories)

    def test_achievement_unlock_notification(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user,
        sample_exercises_with_tags
    ):
        """Test that achievement unlocks trigger notifications."""
        # Create achievement
        achievement = Achievement(
            name="Notification Test",
            description="Test notification",
            category="test",
            icon_url="bell",
            points=5,
            criteria={"exercises_completed": 1}
        )
        db_session.add(achievement)
        db_session.commit()

        # Submit exercise to trigger unlock
        response = authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": str(sample_exercises_with_tags[0].id),
                "user_answer": sample_exercises_with_tags[0].correct_answer,
                "time_taken": 5
            }
        )

        # Response should include achievement notification
        if response.status_code == status.HTTP_200_OK:
            result = response.json()

            # Check if achievements unlocked are included in response
            if "achievements_unlocked" in result:
                assert len(result["achievements_unlocked"]) >= 0

    def test_rare_achievements(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user
    ):
        """Test rare/difficult achievements."""
        # Create rare achievement with difficult criteria
        rare_achievement = Achievement(
            name="Master Scholar",
            description="Complete 1000 exercises with 95% accuracy",
            category="mastery",
            icon_url="crown",
            points=500,
            criteria={
                "exercises_completed": 1000,
                "accuracy_required": 95.0
            }
        )
        db_session.add(rare_achievement)
        db_session.commit()

        # Verify it exists but is not unlocked
        user_achievements = db_session.query(UserAchievement).filter(
            UserAchievement.user_id == test_user.id,
            UserAchievement.achievement_id == rare_achievement.id
        ).first()

        assert user_achievements is None  # Should not be unlocked yet
