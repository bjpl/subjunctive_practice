"""
Tests for spaced repetition review endpoints.
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.models.exercise import Verb, VerbType
from backend.models.progress import ReviewSchedule
from backend.models.user import User


def test_get_due_reviews_empty(client: TestClient, test_user_token: str):
    """Test getting due reviews when none exist."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    response = client.get("/api/exercises/review/due", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_due"] == 0
    assert data["items"] == []


def test_get_due_reviews_with_data(
    client: TestClient,
    test_user_token: str,
    db_session: Session,
    test_user: User
):
    """Test getting due reviews with actual data."""
    # Create a test verb
    verb = Verb(
        infinitive="hablar",
        english_translation="to speak",
        verb_type=VerbType.REGULAR,
        present_subjunctive={
            "yo": "hable",
            "tú": "hables",
            "él/ella/usted": "hable"
        }
    )
    db_session.add(verb)
    db_session.flush()
    
    # Create a due review schedule (past due date)
    past_date = datetime.utcnow() - timedelta(days=2)
    review = ReviewSchedule(
        user_id=test_user.id,
        verb_id=verb.id,
        easiness_factor=2.5,
        interval_days=1,
        repetitions=0,
        next_review_date=past_date,
        review_count=0,
        total_correct=0,
        total_attempts=0
    )
    db_session.add(review)
    db_session.commit()
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get("/api/exercises/review/due", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_due"] == 1
    assert len(data["items"]) == 1
    
    item = data["items"][0]
    assert item["verb_infinitive"] == "hablar"
    assert item["verb_translation"] == "to speak"
    assert item["days_overdue"] >= 2
    assert item["difficulty_level"] == "new"


def test_get_due_reviews_with_limit(
    client: TestClient,
    test_user_token: str,
    db_session: Session,
    test_user: User
):
    """Test that limit parameter works correctly."""
    # Create multiple test verbs and reviews
    past_date = datetime.utcnow() - timedelta(days=1)
    
    for i in range(5):
        verb = Verb(
            infinitive=f"verb{i}",
            english_translation=f"to verb{i}",
            verb_type=VerbType.REGULAR,
            present_subjunctive={"yo": f"verb{i}e"}
        )
        db_session.add(verb)
        db_session.flush()
        
        review = ReviewSchedule(
            user_id=test_user.id,
            verb_id=verb.id,
            easiness_factor=2.5,
            interval_days=1,
            repetitions=0,
            next_review_date=past_date,
            review_count=0,
            total_correct=0,
            total_attempts=0
        )
        db_session.add(review)
    
    db_session.commit()
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get("/api/exercises/review/due?limit=3", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3


def test_get_review_stats_empty(client: TestClient, test_user_token: str):
    """Test getting review stats when no data exists."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    
    response = client.get("/api/exercises/review/stats", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_due"] == 0
    assert data["average_retention"] == 0.0
    assert data["total_reviewed"] == 0


def test_get_review_stats_with_data(
    client: TestClient,
    test_user_token: str,
    db_session: Session,
    test_user: User
):
    """Test getting review stats with actual data."""
    # Create test verbs and reviews with varying difficulty
    past_date = datetime.utcnow() - timedelta(days=1)
    future_date = datetime.utcnow() + timedelta(days=3)
    
    # Due item - new
    verb1 = Verb(
        infinitive="hablar",
        english_translation="to speak",
        verb_type=VerbType.REGULAR,
        present_subjunctive={"yo": "hable"}
    )
    db_session.add(verb1)
    db_session.flush()
    
    review1 = ReviewSchedule(
        user_id=test_user.id,
        verb_id=verb1.id,
        easiness_factor=2.5,
        interval_days=1,
        repetitions=0,
        next_review_date=past_date,
        review_count=0,
        total_correct=0,
        total_attempts=0
    )
    db_session.add(review1)
    
    # Due item - learning
    verb2 = Verb(
        infinitive="comer",
        english_translation="to eat",
        verb_type=VerbType.REGULAR,
        present_subjunctive={"yo": "coma"}
    )
    db_session.add(verb2)
    db_session.flush()
    
    review2 = ReviewSchedule(
        user_id=test_user.id,
        verb_id=verb2.id,
        easiness_factor=1.8,  # Learning difficulty
        interval_days=1,
        repetitions=2,
        next_review_date=past_date,
        review_count=2,
        total_correct=4,
        total_attempts=6
    )
    db_session.add(review2)
    
    # Not due item
    verb3 = Verb(
        infinitive="vivir",
        english_translation="to live",
        verb_type=VerbType.REGULAR,
        present_subjunctive={"yo": "viva"}
    )
    db_session.add(verb3)
    db_session.flush()
    
    review3 = ReviewSchedule(
        user_id=test_user.id,
        verb_id=verb3.id,
        easiness_factor=2.6,
        interval_days=7,
        repetitions=5,
        next_review_date=future_date,
        review_count=5,
        total_correct=10,
        total_attempts=10
    )
    db_session.add(review3)
    
    db_session.commit()
    
    headers = {"Authorization": f"Bearer {test_user_token}"}
    response = client.get("/api/exercises/review/stats", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_due"] == 2  # review1 and review2
    assert data["due_by_difficulty"]["new"] == 1
    assert data["due_by_difficulty"]["learning"] == 1
    assert data["total_reviewed"] == 2  # review2 and review3 have review_count > 0
    
    # Average retention: (4 + 10) / (6 + 10) = 14/16 = 87.5%
    assert data["average_retention"] == 87.5


def test_unauthorized_access_to_review_endpoints(client: TestClient):
    """Test that review endpoints require authentication."""
    # Test /review/due without auth
    response = client.get("/api/exercises/review/due")
    assert response.status_code == 401
    
    # Test /review/stats without auth
    response = client.get("/api/exercises/review/stats")
    assert response.status_code == 401
