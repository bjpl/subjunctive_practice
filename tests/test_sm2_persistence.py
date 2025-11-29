"""
Test SM-2 spaced repetition data persistence.

This test verifies that the LearningAlgorithm class correctly
persists SM2Card data to the database using the ReviewSchedule model.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import Base
from models.progress import ReviewSchedule
from models.exercise import Verb, VerbType
from services.learning_algorithm import LearningAlgorithm, SM2Card


def test_sm2_persistence():
    """Test that SM-2 data persists to database correctly."""

    # Create in-memory database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        # Create test verb
        test_verb = Verb(
            infinitive="hablar",
            english_translation="to speak",
            verb_type=VerbType.REGULAR,
            present_subjunctive={
                "yo": "hable",
                "tú": "hables",
                "él/ella/usted": "hable",
                "nosotros": "hablemos",
                "vosotros": "habléis",
                "ellos/ellas/ustedes": "hablen"
            },
            frequency_rank=1,
            is_irregular=False
        )
        db.add(test_verb)
        db.commit()
        db.refresh(test_verb)

        # Create LearningAlgorithm with database session
        learning_algo = LearningAlgorithm(db_session=db)

        # Test user
        user_id = 1

        # Process first exercise result
        result1 = learning_algo.process_exercise_result(
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            correct=True,
            response_time_ms=3000,
            user_id=user_id
        )

        print("✓ First exercise processed")
        print(f"  - Next review: {result1['next_review']}")
        print(f"  - Interval days: {result1['interval_days']}")

        # Verify data was saved to database
        review = db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id,
            ReviewSchedule.verb_id == test_verb.id
        ).first()

        assert review is not None, "ReviewSchedule should be created"
        assert review.easiness_factor > 0, "Easiness factor should be set"
        assert review.interval_days > 0, "Interval should be set"
        assert review.total_attempts == 1, "Should have 1 attempt"
        assert review.total_correct == 1, "Should have 1 correct"

        print("✓ Data persisted to database")
        print(f"  - EF: {review.easiness_factor}")
        print(f"  - Interval: {review.interval_days} days")
        print(f"  - Attempts: {review.total_attempts}")
        print(f"  - Correct: {review.total_correct}")

        # Create new instance to simulate new request
        learning_algo2 = LearningAlgorithm(db_session=db)

        # Process second exercise result
        result2 = learning_algo2.process_exercise_result(
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            correct=True,
            response_time_ms=2500,
            user_id=user_id
        )

        print("\n✓ Second exercise processed")
        print(f"  - Next review: {result2['next_review']}")
        print(f"  - Interval days: {result2['interval_days']}")

        # Verify data was updated
        db.refresh(review)

        assert review.total_attempts == 2, "Should have 2 attempts"
        assert review.total_correct == 2, "Should have 2 correct"
        assert review.interval_days >= result1['interval_days'], "Interval should increase"

        print("✓ Data updated correctly")
        print(f"  - EF: {review.easiness_factor}")
        print(f"  - Interval: {review.interval_days} days")
        print(f"  - Attempts: {review.total_attempts}")
        print(f"  - Correct: {review.total_correct}")

        # Test loading card from database
        learning_algo3 = LearningAlgorithm(db_session=db)
        card = learning_algo3.load_card_from_db(
            user_id=user_id,
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        assert card is not None, "Should load card from database"
        assert card.total_reviews == 2, "Should have 2 reviews"
        assert card.correct_reviews == 2, "Should have 2 correct"

        print("\n✓ Card loaded from database successfully")
        print(f"  - Total reviews: {card.total_reviews}")
        print(f"  - Correct: {card.correct_reviews}")
        print(f"  - Accuracy: {card.get_accuracy():.1f}%")

        # Test incorrect answer
        result3 = learning_algo3.process_exercise_result(
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            correct=False,
            response_time_ms=8000,
            user_id=user_id
        )

        print("\n✓ Incorrect answer processed")
        print(f"  - Interval reset to: {result3['interval_days']} days")

        db.refresh(review)
        assert review.total_attempts == 3, "Should have 3 attempts"
        assert review.total_correct == 2, "Should still have 2 correct"

        print("✓ All tests passed!")
        print("\n" + "="*60)
        print("SM-2 PERSISTENCE TEST SUCCESSFUL")
        print("="*60)

    finally:
        db.close()


if __name__ == "__main__":
    test_sm2_persistence()
