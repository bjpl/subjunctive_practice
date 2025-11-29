"""
Learning Algorithms Module

Implements spaced repetition (SM-2 algorithm), adaptive difficulty,
and progress tracking for optimal learning retention.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import math
import logging


logger = logging.getLogger(__name__)


@dataclass
class SM2Card:
    """
    Represents a flashcard item for SM-2 spaced repetition.

    Based on SuperMemo 2 (SM-2) algorithm by Piotr Wozniak.
    """
    item_id: str
    verb: str
    tense: str
    person: str
    easiness_factor: float = 2.5  # Initial EF (1.3 - 2.5 range)
    interval: int = 0  # Days until next review
    repetitions: int = 0  # Number of successful repetitions
    next_review: datetime = field(default_factory=datetime.now)
    last_review: Optional[datetime] = None
    total_reviews: int = 0
    correct_reviews: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "item_id": self.item_id,
            "verb": self.verb,
            "tense": self.tense,
            "person": self.person,
            "easiness_factor": self.easiness_factor,
            "interval": self.interval,
            "repetitions": self.repetitions,
            "next_review": self.next_review.isoformat(),
            "last_review": self.last_review.isoformat() if self.last_review else None,
            "total_reviews": self.total_reviews,
            "correct_reviews": self.correct_reviews,
            "created_at": self.created_at.isoformat(),
            "accuracy": self.get_accuracy()
        }

    def get_accuracy(self) -> float:
        """Calculate accuracy percentage"""
        if self.total_reviews == 0:
            return 0.0
        return (self.correct_reviews / self.total_reviews) * 100


class SM2Algorithm:
    """
    Implementation of SuperMemo 2 (SM-2) spaced repetition algorithm.

    The algorithm schedules reviews based on:
    - Quality of recall (0-5 scale)
    - Easiness factor (measures how easy item is to remember)
    - Repetition number
    - Previous interval

    Reference: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def calculate_next_interval(
        self,
        card: SM2Card,
        quality: int
    ) -> Tuple[int, float, int, datetime]:
        """
        Calculate next review interval using SM-2 algorithm.

        Args:
            card: SM2Card object
            quality: Quality of recall (0-5)
                5 = perfect response
                4 = correct response after hesitation
                3 = correct response with difficulty
                2 = incorrect but remembered
                1 = incorrect, familiar
                0 = complete blackout

        Returns:
            Tuple of (new_interval, new_easiness_factor, new_repetitions, next_review_date)
        """
        # Validate quality
        if quality < 0 or quality > 5:
            raise ValueError("Quality must be between 0 and 5")

        # Copy current values
        ef = card.easiness_factor
        repetitions = card.repetitions
        interval = card.interval

        # Update easiness factor
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

        # Ensure EF stays within bounds
        if ef < 1.3:
            ef = 1.3

        # If quality < 3, reset repetitions
        if quality < 3:
            repetitions = 0
            interval = 1
        else:
            repetitions += 1

            # Calculate interval based on repetition number
            if repetitions == 1:
                interval = 1
            elif repetitions == 2:
                interval = 6
            else:
                interval = round(interval * ef)

        # Calculate next review date
        next_review = datetime.now() + timedelta(days=interval)

        return interval, ef, repetitions, next_review

    def process_review(
        self,
        card: SM2Card,
        correct: bool,
        response_time_ms: int,
        difficulty_felt: Optional[int] = None
    ) -> SM2Card:
        """
        Process a review and update card.

        Args:
            card: SM2Card to update
            correct: Whether answer was correct
            response_time_ms: Time taken to respond in milliseconds
            difficulty_felt: User's perceived difficulty (1-5, optional)

        Returns:
            Updated SM2Card
        """
        # Convert correctness and response time to quality score
        quality = self._calculate_quality_score(
            correct,
            response_time_ms,
            difficulty_felt
        )

        # Calculate new interval using SM-2
        interval, ef, reps, next_review = self.calculate_next_interval(card, quality)

        # Update card
        card.interval = interval
        card.easiness_factor = ef
        card.repetitions = reps
        card.last_review = datetime.now()
        card.next_review = next_review
        card.total_reviews += 1

        if correct:
            card.correct_reviews += 1

        self.logger.info(
            f"Updated card {card.item_id}: "
            f"quality={quality}, interval={interval}, EF={ef:.2f}, next={next_review}"
        )

        return card

    def _calculate_quality_score(
        self,
        correct: bool,
        response_time_ms: int,
        difficulty_felt: Optional[int] = None
    ) -> int:
        """
        Calculate SM-2 quality score (0-5) from review data.

        Args:
            correct: Whether answer was correct
            response_time_ms: Response time in milliseconds
            difficulty_felt: User's perceived difficulty (1-5)

        Returns:
            Quality score (0-5)
        """
        if not correct:
            # Incorrect answers: 0-2
            if difficulty_felt and difficulty_felt >= 4:
                return 0  # Complete blackout
            elif response_time_ms > 15000:
                return 0  # Took too long, probably guessed
            elif response_time_ms > 10000:
                return 1  # Incorrect but some familiarity
            else:
                return 2  # Incorrect but remembered something

        # Correct answers: 3-5
        # Base score on response time and difficulty
        if difficulty_felt:
            # User explicitly indicated difficulty
            if difficulty_felt <= 2:
                return 5  # Easy
            elif difficulty_felt == 3:
                return 4  # Medium
            else:
                return 3  # Hard

        # Estimate from response time
        # Fast response (< 3 sec) = 5
        # Medium response (3-7 sec) = 4
        # Slow response (> 7 sec) = 3
        if response_time_ms < 3000:
            return 5
        elif response_time_ms < 7000:
            return 4
        else:
            return 3

    def get_due_cards(
        self,
        cards: List[SM2Card],
        count: Optional[int] = None
    ) -> List[SM2Card]:
        """
        Get cards that are due for review.

        Args:
            cards: List of SM2Card objects
            count: Maximum number of cards to return (None = all due)

        Returns:
            List of due cards, sorted by next_review date
        """
        now = datetime.now()
        due_cards = [card for card in cards if card.next_review <= now]

        # Sort by next_review date (oldest first)
        due_cards.sort(key=lambda c: c.next_review)

        if count is not None:
            return due_cards[:count]

        return due_cards


class AdaptiveDifficultyManager:
    """
    Manages adaptive difficulty adjustment based on user performance.

    Adjusts difficulty level based on:
    - Recent accuracy
    - Response times
    - Streak of correct/incorrect answers
    - Learning velocity
    """

    def __init__(
        self,
        initial_difficulty: str = "intermediate",
        adjustment_threshold: int = 10
    ):
        """
        Initialize adaptive difficulty manager.

        Args:
            initial_difficulty: Starting difficulty level
            adjustment_threshold: Number of exercises before considering adjustment
        """
        self.difficulty = initial_difficulty
        self.adjustment_threshold = adjustment_threshold
        self.recent_results: List[bool] = []
        self.recent_times: List[int] = []
        self.logger = logging.getLogger(__name__)

    def record_result(
        self,
        correct: bool,
        response_time_ms: int
    ) -> Optional[str]:
        """
        Record an exercise result and potentially adjust difficulty.

        Args:
            correct: Whether answer was correct
            response_time_ms: Time taken in milliseconds

        Returns:
            New difficulty level if changed, None otherwise
        """
        self.recent_results.append(correct)
        self.recent_times.append(response_time_ms)

        # Keep only recent history
        if len(self.recent_results) > self.adjustment_threshold:
            self.recent_results = self.recent_results[-self.adjustment_threshold:]
            self.recent_times = self.recent_times[-self.adjustment_threshold:]

        # Check if we should adjust
        if len(self.recent_results) >= self.adjustment_threshold:
            new_difficulty = self._calculate_difficulty()

            if new_difficulty != self.difficulty:
                old_difficulty = self.difficulty
                self.difficulty = new_difficulty
                self.logger.info(
                    f"Difficulty adjusted: {old_difficulty} -> {new_difficulty}"
                )
                return new_difficulty

        return None

    def _calculate_difficulty(self) -> str:
        """Calculate appropriate difficulty level"""
        # Calculate metrics
        accuracy = sum(self.recent_results) / len(self.recent_results)
        avg_time = sum(self.recent_times) / len(self.recent_times)

        # Get current difficulty index
        levels = ["beginner", "intermediate", "advanced"]
        current_index = levels.index(self.difficulty)

        # Decision logic
        # Increase difficulty if: high accuracy + fast times
        if accuracy >= 0.85 and avg_time < 5000:
            if current_index < len(levels) - 1:
                return levels[current_index + 1]

        # Decrease difficulty if: low accuracy
        elif accuracy < 0.60:
            if current_index > 0:
                return levels[current_index - 1]

        # Stay at current level
        return self.difficulty

    def get_difficulty(self) -> str:
        """Get current difficulty level"""
        return self.difficulty

    def get_performance_metrics(self) -> Dict:
        """Get current performance metrics"""
        if not self.recent_results:
            return {
                "accuracy": 0.0,
                "average_time_ms": 0,
                "sample_size": 0,
                "difficulty": self.difficulty
            }

        return {
            "accuracy": sum(self.recent_results) / len(self.recent_results),
            "average_time_ms": sum(self.recent_times) / len(self.recent_times),
            "sample_size": len(self.recent_results),
            "difficulty": self.difficulty
        }


class LearningAlgorithm:
    """
    Main learning algorithm coordinator.

    Combines:
    - SM-2 spaced repetition
    - Adaptive difficulty
    - Progress tracking
    - Learning analytics
    """

    def __init__(
        self,
        initial_difficulty: str = "intermediate",
        db_session = None
    ):
        """
        Initialize learning algorithm.

        Args:
            initial_difficulty: Starting difficulty level
            db_session: SQLAlchemy database session for persistence (optional)
        """
        self.sm2 = SM2Algorithm()
        self.difficulty_manager = AdaptiveDifficultyManager(initial_difficulty)
        self.cards: Dict[str, SM2Card] = {}
        self.db = db_session
        self.logger = logging.getLogger(__name__)

    def load_card_from_db(
        self,
        user_id: int,
        verb: str,
        tense: str,
        person: str
    ) -> Optional[SM2Card]:
        """
        Load SM2Card from database ReviewSchedule.

        Args:
            user_id: User ID
            verb: Verb infinitive
            tense: Subjunctive tense
            person: Grammatical person

        Returns:
            SM2Card if found in database, None otherwise
        """
        if not self.db:
            return None

        from models.progress import ReviewSchedule
        from models.exercise import Verb

        # Get verb_id from verb infinitive
        verb_obj = self.db.query(Verb).filter(Verb.infinitive == verb).first()
        if not verb_obj:
            self.logger.warning(f"Verb '{verb}' not found in database")
            return None

        # Query ReviewSchedule
        # Note: ReviewSchedule stores per-verb data, not per verb+tense+person
        # We'll use the verb_id and store tense/person info in a JSON field if needed
        # For now, we'll create separate records per combination by using verb_id
        review = self.db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id,
            ReviewSchedule.verb_id == verb_obj.id
        ).first()

        if not review:
            return None

        # Convert ReviewSchedule to SM2Card
        item_id = f"{verb}_{tense}_{person}"
        card = SM2Card(
            item_id=item_id,
            verb=verb,
            tense=tense,
            person=person,
            easiness_factor=review.easiness_factor,
            interval=review.interval_days,
            repetitions=review.repetitions,
            next_review=review.next_review_date,
            last_review=review.last_reviewed_at,
            total_reviews=review.total_attempts,
            correct_reviews=review.total_correct,
            created_at=review.created_at
        )

        self.logger.info(f"Loaded card from DB: {item_id}")
        return card

    def save_card_to_db(
        self,
        user_id: int,
        card: SM2Card
    ) -> None:
        """
        Save SM2Card to database ReviewSchedule.

        Args:
            user_id: User ID
            card: SM2Card to save
        """
        if not self.db:
            self.logger.warning("No database session available, skipping save")
            return

        from models.progress import ReviewSchedule
        from models.exercise import Verb

        # Get verb_id
        verb_obj = self.db.query(Verb).filter(Verb.infinitive == card.verb).first()
        if not verb_obj:
            self.logger.error(f"Cannot save card: verb '{card.verb}' not found in database")
            return

        # Check if ReviewSchedule exists
        review = self.db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id,
            ReviewSchedule.verb_id == verb_obj.id
        ).first()

        if review:
            # Update existing record
            review.easiness_factor = card.easiness_factor
            review.interval_days = card.interval
            review.repetitions = card.repetitions
            review.next_review_date = card.next_review
            review.last_reviewed_at = card.last_review
            review.review_count = card.total_reviews
            review.total_attempts = card.total_reviews
            review.total_correct = card.correct_reviews
            review.updated_at = datetime.now()

            self.logger.info(f"Updated ReviewSchedule for user {user_id}, verb {card.verb}")
        else:
            # Create new record
            review = ReviewSchedule(
                user_id=user_id,
                verb_id=verb_obj.id,
                easiness_factor=card.easiness_factor,
                interval_days=card.interval,
                repetitions=card.repetitions,
                next_review_date=card.next_review,
                last_reviewed_at=card.last_review,
                review_count=card.total_reviews,
                total_attempts=card.total_reviews,
                total_correct=card.correct_reviews,
                created_at=card.created_at
            )
            self.db.add(review)
            self.logger.info(f"Created ReviewSchedule for user {user_id}, verb {card.verb}")

        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to save ReviewSchedule: {e}")
            raise

    def add_card(
        self,
        verb: str,
        tense: str,
        person: str,
        user_id: Optional[int] = None
    ) -> SM2Card:
        """
        Add a new card to the learning system.

        Args:
            verb: Verb infinitive
            tense: Subjunctive tense
            person: Grammatical person
            user_id: User ID for database persistence (optional)

        Returns:
            Created SM2Card
        """
        item_id = f"{verb}_{tense}_{person}"

        # Check in-memory cache first
        if item_id in self.cards:
            return self.cards[item_id]

        # Try loading from database if user_id provided
        if user_id and self.db:
            card = self.load_card_from_db(user_id, verb, tense, person)
            if card:
                self.cards[item_id] = card
                return card

        # Create new card
        card = SM2Card(
            item_id=item_id,
            verb=verb,
            tense=tense,
            person=person
        )

        self.cards[item_id] = card
        self.logger.info(f"Added new card: {item_id}")

        return card

    def process_exercise_result(
        self,
        verb: str,
        tense: str,
        person: str,
        correct: bool,
        response_time_ms: int,
        difficulty_felt: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> Dict:
        """
        Process an exercise result and update learning state.

        Args:
            verb: Verb infinitive
            tense: Subjunctive tense
            person: Grammatical person
            correct: Whether answer was correct
            response_time_ms: Response time in milliseconds
            difficulty_felt: User's perceived difficulty (1-5)
            user_id: User ID for database persistence (optional)

        Returns:
            Dictionary with update results
        """
        # Get or create card
        item_id = f"{verb}_{tense}_{person}"
        card = self.cards.get(item_id) or self.add_card(verb, tense, person, user_id)

        # Update card with SM-2
        updated_card = self.sm2.process_review(
            card,
            correct,
            response_time_ms,
            difficulty_felt
        )

        self.cards[item_id] = updated_card

        # Save to database if user_id provided
        if user_id and self.db:
            try:
                self.save_card_to_db(user_id, updated_card)
            except Exception as e:
                self.logger.error(f"Failed to persist card to database: {e}")

        # Update difficulty
        new_difficulty = self.difficulty_manager.record_result(
            correct,
            response_time_ms
        )

        return {
            "card_updated": updated_card.to_dict(),
            "difficulty_changed": new_difficulty is not None,
            "new_difficulty": new_difficulty or self.difficulty_manager.get_difficulty(),
            "next_review": updated_card.next_review.isoformat(),
            "interval_days": updated_card.interval
        }

    def get_next_items(self, count: int = 10) -> List[SM2Card]:
        """
        Get next items for practice.

        Returns due items first, then new items.

        Args:
            count: Number of items to return

        Returns:
            List of SM2Card objects
        """
        all_cards = list(self.cards.values())

        # Get due cards
        due_cards = self.sm2.get_due_cards(all_cards, count)

        if len(due_cards) >= count:
            return due_cards

        # Add new cards if needed
        new_cards = [c for c in all_cards if c.total_reviews == 0]
        new_cards.sort(key=lambda c: c.created_at)

        remaining = count - len(due_cards)
        return due_cards + new_cards[:remaining]

    def get_statistics(self) -> Dict:
        """Get learning statistics"""
        if not self.cards:
            return {
                "total_cards": 0,
                "mastered_cards": 0,
                "learning_cards": 0,
                "new_cards": 0,
                "due_cards": 0,
                "overall_accuracy": 0.0,
                "difficulty": self.difficulty_manager.get_difficulty()
            }

        all_cards = list(self.cards.values())

        # Categorize cards
        new_cards = [c for c in all_cards if c.total_reviews == 0]
        learning_cards = [c for c in all_cards if 0 < c.repetitions < 5]
        mastered_cards = [c for c in all_cards if c.repetitions >= 5]
        due_cards = self.sm2.get_due_cards(all_cards)

        # Calculate overall accuracy
        total_reviews = sum(c.total_reviews for c in all_cards)
        total_correct = sum(c.correct_reviews for c in all_cards)
        overall_accuracy = (total_correct / total_reviews * 100) if total_reviews > 0 else 0.0

        return {
            "total_cards": len(all_cards),
            "mastered_cards": len(mastered_cards),
            "learning_cards": len(learning_cards),
            "new_cards": len(new_cards),
            "due_cards": len(due_cards),
            "overall_accuracy": overall_accuracy,
            "difficulty": self.difficulty_manager.get_difficulty(),
            "performance_metrics": self.difficulty_manager.get_performance_metrics()
        }


# Example usage
if __name__ == "__main__":
    # Initialize learning algorithm
    learning = LearningAlgorithm(initial_difficulty="intermediate")

    # Add some cards
    learning.add_card("hablar", "present_subjunctive", "yo")
    learning.add_card("ser", "present_subjunctive", "yo")
    learning.add_card("tener", "present_subjunctive", "yo")

    # Process exercise results
    result = learning.process_exercise_result(
        verb="hablar",
        tense="present_subjunctive",
        person="yo",
        correct=True,
        response_time_ms=2500
    )

    print(f"Card updated: {result['card_updated']['item_id']}")
    print(f"Next review: {result['next_review']}")
    print(f"Interval: {result['interval_days']} days")

    # Get statistics
    stats = learning.get_statistics()
    print(f"\nStatistics:")
    print(f"Total cards: {stats['total_cards']}")
    print(f"Due cards: {stats['due_cards']}")
    print(f"Accuracy: {stats['overall_accuracy']:.1f}%")
