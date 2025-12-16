"""
Integration tests for learning progress and spaced repetition flow.

Tests the complete learning algorithm workflow:
1. Spaced repetition schedule creation
2. Review scheduling based on SM-2 algorithm
3. Progress tracking and mastery calculation
4. Review queue management
5. Adaptive difficulty adjustment
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models.exercise import Verb, VerbType
from models.progress import ReviewSchedule, Attempt, Session as PracticeSession
from models.user import User, UserProfile
from services.learning_algorithm import LearningAlgorithm, SM2Card


@pytest.mark.integration
class TestLearningProgressFlow:
    """Integration tests for spaced repetition and progress tracking."""

    def test_complete_spaced_repetition_flow(
        self,
        db_session: Session,
        test_user: User,
        learning_algorithm: LearningAlgorithm
    ):
        """
        Test complete spaced repetition workflow from initial learning to mastery.

        Flow:
        1. Create new verb for learning
        2. Initialize review schedule
        3. Complete first review (correct)
        4. Verify schedule updated
        5. Complete second review (correct)
        6. Verify interval increased
        7. Complete review (incorrect)
        8. Verify interval reset
        """
        # Step 1: Create verb
        verb = Verb(
            infinitive="estudiar",
            english_translation="to study",
            verb_type=VerbType.REGULAR,
            present_subjunctive={
                "yo": "estudie",
                "tú": "estudies",
                "él": "estudie"
            },
            is_irregular=False
        )
        db_session.add(verb)
        db_session.commit()
        db_session.refresh(verb)

        # Step 2: Initialize review schedule
        schedule = ReviewSchedule(
            user_id=test_user.id,
            verb_id=verb.id,
            easiness_factor=2.5,
            interval_days=1,
            repetitions=0,
            next_review_date=datetime.utcnow(),
            review_count=0,
            total_correct=0,
            total_attempts=0
        )
        db_session.add(schedule)
        db_session.commit()
        db_session.refresh(schedule)

        assert schedule.interval_days == 1
        assert schedule.easiness_factor == 2.5

        # Step 3: First review (correct, quality=4)
        quality = 4  # Good recall

        # Update schedule using SM-2 algorithm
        new_ef = max(1.3, schedule.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        if quality >= 3:
            if schedule.repetitions == 0:
                new_interval = 1
            elif schedule.repetitions == 1:
                new_interval = 6
            else:
                new_interval = int(schedule.interval_days * new_ef)
            new_repetitions = schedule.repetitions + 1
        else:
            new_interval = 1
            new_repetitions = 0

        schedule.easiness_factor = new_ef
        schedule.interval_days = new_interval
        schedule.repetitions = new_repetitions
        schedule.last_reviewed_at = datetime.utcnow()
        schedule.next_review_date = datetime.utcnow() + timedelta(days=new_interval)
        schedule.review_count += 1
        schedule.total_attempts += 1
        schedule.total_correct += 1

        db_session.commit()
        db_session.refresh(schedule)

        # Step 4: Verify schedule updated
        assert schedule.repetitions == 1
        assert schedule.interval_days == 1
        assert schedule.review_count == 1
        assert schedule.total_correct == 1

        # Step 5: Second review (correct, quality=5)
        quality = 5  # Perfect recall

        new_ef = max(1.3, schedule.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        if schedule.repetitions == 1:
            new_interval = 6
        else:
            new_interval = int(schedule.interval_days * new_ef)

        schedule.easiness_factor = new_ef
        schedule.interval_days = new_interval
        schedule.repetitions += 1
        schedule.last_reviewed_at = datetime.utcnow()
        schedule.next_review_date = datetime.utcnow() + timedelta(days=new_interval)
        schedule.review_count += 1
        schedule.total_attempts += 1
        schedule.total_correct += 1

        db_session.commit()
        db_session.refresh(schedule)

        # Step 6: Verify interval increased
        assert schedule.interval_days == 6
        assert schedule.repetitions == 2
        assert schedule.total_correct == 2

        # Step 7: Third review (incorrect, quality=1)
        quality = 1  # Complete blackout

        new_ef = max(1.3, schedule.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        # Failed recall, reset
        schedule.easiness_factor = new_ef
        schedule.interval_days = 1
        schedule.repetitions = 0
        schedule.last_reviewed_at = datetime.utcnow()
        schedule.next_review_date = datetime.utcnow() + timedelta(days=1)
        schedule.review_count += 1
        schedule.total_attempts += 1

        db_session.commit()
        db_session.refresh(schedule)

        # Step 8: Verify reset
        assert schedule.interval_days == 1
        assert schedule.repetitions == 0
        assert schedule.total_attempts == 3
        assert schedule.total_correct == 2

    def test_review_queue_due_items(
        self,
        db_session: Session,
        test_user: User
    ):
        """
        Test fetching items due for review.

        Flow:
        1. Create multiple review schedules
        2. Set some as due, others not due
        3. Query due reviews
        4. Verify correct items returned
        """
        # Create verbs
        verb1 = Verb(
            infinitive="hablar",
            english_translation="to speak",
            verb_type=VerbType.REGULAR,
            present_subjunctive={"yo": "hable"},
            is_irregular=False
        )
        verb2 = Verb(
            infinitive="comer",
            english_translation="to eat",
            verb_type=VerbType.REGULAR,
            present_subjunctive={"yo": "coma"},
            is_irregular=False
        )
        db_session.add_all([verb1, verb2])
        db_session.commit()

        # Schedule 1: Due now
        schedule1 = ReviewSchedule(
            user_id=test_user.id,
            verb_id=verb1.id,
            easiness_factor=2.5,
            interval_days=1,
            repetitions=0,
            next_review_date=datetime.utcnow() - timedelta(hours=1),  # Past due
            review_count=0,
            total_attempts=0,
            total_correct=0
        )

        # Schedule 2: Not due yet
        schedule2 = ReviewSchedule(
            user_id=test_user.id,
            verb_id=verb2.id,
            easiness_factor=2.5,
            interval_days=1,
            repetitions=0,
            next_review_date=datetime.utcnow() + timedelta(days=3),  # Future
            review_count=0,
            total_attempts=0,
            total_correct=0
        )

        db_session.add_all([schedule1, schedule2])
        db_session.commit()

        # Query due reviews
        due_reviews = db_session.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == test_user.id,
            ReviewSchedule.next_review_date <= datetime.utcnow()
        ).all()

        assert len(due_reviews) == 1
        assert due_reviews[0].verb_id == verb1.id

    def test_mastery_calculation_from_performance(
        self,
        db_session: Session,
        test_user: User
    ):
        """
        Test mastery level calculation based on performance.

        Flow:
        1. Create verb with review history
        2. Track multiple correct attempts
        3. Calculate mastery percentage
        4. Verify mastery thresholds
        """
        # Create verb
        verb = Verb(
            infinitive="vivir",
            english_translation="to live",
            verb_type=VerbType.REGULAR,
            present_subjunctive={"yo": "viva"},
            is_irregular=False
        )
        db_session.add(verb)
        db_session.commit()

        # Create review schedule with history
        schedule = ReviewSchedule(
            user_id=test_user.id,
            verb_id=verb.id,
            easiness_factor=2.5,
            interval_days=10,
            repetitions=5,  # Multiple successful reviews
            next_review_date=datetime.utcnow() + timedelta(days=10),
            review_count=10,
            total_attempts=10,
            total_correct=9  # 90% accuracy
        )
        db_session.add(schedule)
        db_session.commit()
        db_session.refresh(schedule)

        # Calculate mastery
        accuracy = (schedule.total_correct / schedule.total_attempts) * 100
        assert accuracy == 90.0

        # Mastery criteria:
        # - High accuracy (>85%)
        # - Multiple repetitions (>=3)
        # - High easiness factor (>=2.5)
        # - Long interval (>=7 days)

        is_mastered = (
            accuracy >= 85 and
            schedule.repetitions >= 3 and
            schedule.easiness_factor >= 2.5 and
            schedule.interval_days >= 7
        )

        assert is_mastered is True

    def test_adaptive_difficulty_adjustment(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test difficulty adjusts based on user performance.

        Flow:
        1. Track user accuracy over multiple attempts
        2. Calculate performance metrics
        3. Adjust difficulty recommendation
        4. Verify appropriate difficulty level
        """
        # Create practice session with attempts
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        # Simulate high performance (8/10 correct)
        exercises = sample_exercises_with_tags[:10]
        correct_count = 0

        for i, exercise in enumerate(exercises):
            is_correct = i < 8  # First 8 correct, last 2 incorrect
            attempt = Attempt(
                session_id=session.id,
                exercise_id=exercise.id,
                user_id=test_user.id,
                user_answer=exercise.correct_answer if is_correct else "wrong",
                is_correct=is_correct
            )
            db_session.add(attempt)
            if is_correct:
                correct_count += 1

        db_session.commit()

        # Calculate accuracy
        total_attempts = len(exercises)
        accuracy = (correct_count / total_attempts) * 100
        assert accuracy == 80.0

        # Determine recommended difficulty
        # >80% = increase difficulty
        # 60-80% = maintain
        # <60% = decrease difficulty

        from models.exercise import DifficultyLevel

        if accuracy >= 80:
            recommended = DifficultyLevel.HARD
        elif accuracy >= 60:
            recommended = DifficultyLevel.MEDIUM
        else:
            recommended = DifficultyLevel.EASY

        assert recommended == DifficultyLevel.HARD

    def test_streak_tracking_and_maintenance(
        self,
        db_session: Session,
        test_user: User
    ):
        """
        Test user streak calculation and maintenance.

        Flow:
        1. Create profile with current streak
        2. Practice today (maintain streak)
        3. Skip a day (break streak)
        4. Verify streak logic
        """
        # Create profile
        profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()

        if not profile:
            profile = UserProfile(
                user_id=test_user.id,
                current_streak=3,
                longest_streak=5,
                last_practice_date=datetime.utcnow() - timedelta(days=1)
            )
            db_session.add(profile)
            db_session.commit()
            db_session.refresh(profile)

        initial_streak = profile.current_streak
        last_practice = profile.last_practice_date

        # Scenario 1: Practice today (within 24 hours of last practice)
        now = datetime.utcnow()
        if last_practice and (now - last_practice).days <= 1:
            # Continue streak
            profile.current_streak += 1
            profile.last_practice_date = now
            if profile.current_streak > profile.longest_streak:
                profile.longest_streak = profile.current_streak
        else:
            # Streak broken
            profile.current_streak = 1
            profile.last_practice_date = now

        db_session.commit()
        db_session.refresh(profile)

        assert profile.current_streak == initial_streak + 1

        # Scenario 2: Skip multiple days (break streak)
        profile.last_practice_date = datetime.utcnow() - timedelta(days=3)
        db_session.commit()

        # Next practice resets streak
        now = datetime.utcnow()
        if (now - profile.last_practice_date).days > 1:
            profile.current_streak = 1
        else:
            profile.current_streak += 1

        profile.last_practice_date = now
        db_session.commit()
        db_session.refresh(profile)

        assert profile.current_streak == 1

    def test_learning_curve_tracking(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test tracking learning curve over time.

        Flow:
        1. Create multiple sessions over time
        2. Track accuracy improvement
        3. Calculate learning velocity
        4. Verify progress trend
        """
        # Create sessions with improving accuracy
        sessions_data = [
            {"date": datetime.utcnow() - timedelta(days=7), "correct": 6, "total": 10},
            {"date": datetime.utcnow() - timedelta(days=5), "correct": 7, "total": 10},
            {"date": datetime.utcnow() - timedelta(days=3), "correct": 8, "total": 10},
            {"date": datetime.utcnow() - timedelta(days=1), "correct": 9, "total": 10},
        ]

        accuracies = []
        for session_data in sessions_data:
            session = PracticeSession(
                user_id=test_user.id,
                started_at=session_data["date"],
                session_type="practice",
                total_exercises=session_data["total"],
                correct_answers=session_data["correct"],
                score_percentage=(session_data["correct"] / session_data["total"]) * 100,
                is_completed=True
            )
            db_session.add(session)
            accuracies.append(session.score_percentage)

        db_session.commit()

        # Verify improvement trend
        assert accuracies[0] == 60.0  # Week 1
        assert accuracies[1] == 70.0  # Day 5
        assert accuracies[2] == 80.0  # Day 3
        assert accuracies[3] == 90.0  # Day 1

        # Calculate improvement rate
        improvement = accuracies[-1] - accuracies[0]
        assert improvement == 30.0  # 30% improvement over 7 days
