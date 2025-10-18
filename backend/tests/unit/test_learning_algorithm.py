"""
Unit tests for Learning Algorithm (SM-2 and Adaptive Difficulty).

Tests cover:
- SM-2 spaced repetition algorithm
- Adaptive difficulty adjustment
- Card management
- Progress tracking
- Quality score calculation
"""

import pytest
from datetime import datetime, timedelta
from services.learning_algorithm import (
    SM2Algorithm,
    SM2Card,
    AdaptiveDifficultyManager,
    LearningAlgorithm
)


@pytest.mark.unit
@pytest.mark.learning
class TestSM2Card:
    """Test suite for SM2Card data class."""

    def test_card_creation(self):
        """Test creating SM2 card."""
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        assert card.item_id == "test_1"
        assert card.verb == "hablar"
        assert card.easiness_factor == 2.5
        assert card.interval == 0
        assert card.repetitions == 0

    def test_card_to_dict(self):
        """Test converting card to dictionary."""
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        card_dict = card.to_dict()

        assert isinstance(card_dict, dict)
        assert card_dict["item_id"] == "test_1"
        assert card_dict["verb"] == "hablar"
        assert "accuracy" in card_dict

    def test_card_accuracy_calculation(self):
        """Test accuracy calculation."""
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            total_reviews=10,
            correct_reviews=7
        )

        assert card.get_accuracy() == 70.0

    def test_card_accuracy_no_reviews(self):
        """Test accuracy with no reviews."""
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        assert card.get_accuracy() == 0.0


@pytest.mark.unit
@pytest.mark.learning
class TestSM2Algorithm:
    """Test suite for SM2Algorithm."""

    def test_algorithm_initialization(self):
        """Test algorithm initializes correctly."""
        sm2 = SM2Algorithm()
        assert sm2 is not None

    # ========================================================================
    # Interval Calculation Tests
    # ========================================================================

    @pytest.mark.parametrize("quality,expected_interval", [
        (5, 1),   # Perfect: interval = 1
        (4, 1),   # Good: interval = 1
        (3, 1),   # OK: interval = 1
        (2, 1),   # Poor: reset to 1
        (1, 1),   # Bad: reset to 1
        (0, 1),   # Fail: reset to 1
    ])
    def test_first_repetition_intervals(self, quality, expected_interval):
        """Test interval calculation for first repetition."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        interval, ef, reps, next_review = sm2.calculate_next_interval(card, quality)

        if quality >= 3:
            assert reps == 1
        else:
            assert reps == 0

        assert interval == expected_interval

    def test_second_repetition_interval(self):
        """Test interval for second repetition."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            repetitions=1,
            interval=1
        )

        interval, ef, reps, next_review = sm2.calculate_next_interval(card, 4)

        assert interval == 6  # Second repetition
        assert reps == 2

    def test_subsequent_repetition_interval(self):
        """Test interval for subsequent repetitions."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            repetitions=2,
            interval=6,
            easiness_factor=2.5
        )

        interval, ef, reps, next_review = sm2.calculate_next_interval(card, 4)

        assert interval == round(6 * 2.5)  # interval * EF
        assert reps == 3

    # ========================================================================
    # Easiness Factor Tests
    # ========================================================================

    @pytest.mark.parametrize("quality", [0, 1, 2, 3, 4, 5])
    def test_easiness_factor_adjustment(self, quality):
        """Test EF adjusts based on quality."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            easiness_factor=2.5
        )

        interval, ef, reps, next_review = sm2.calculate_next_interval(card, quality)

        # EF should change based on quality
        if quality >= 4:
            assert ef >= 2.5  # Should increase or stay same
        elif quality < 3:
            assert ef <= 2.5  # Should decrease or stay same

    def test_easiness_factor_minimum(self):
        """Test EF doesn't go below 1.3."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            easiness_factor=1.3
        )

        # Very poor quality should not reduce EF below 1.3
        interval, ef, reps, next_review = sm2.calculate_next_interval(card, 0)

        assert ef >= 1.3

    # ========================================================================
    # Reset on Poor Performance Tests
    # ========================================================================

    @pytest.mark.parametrize("quality", [0, 1, 2])
    def test_reset_on_poor_performance(self, quality):
        """Test repetitions reset on poor quality."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            repetitions=5,
            interval=30
        )

        interval, ef, reps, next_review = sm2.calculate_next_interval(card, quality)

        assert reps == 0  # Reset
        assert interval == 1  # Back to start

    # ========================================================================
    # Process Review Tests
    # ========================================================================

    def test_process_review_correct(self):
        """Test processing correct review."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        updated_card = sm2.process_review(card, correct=True, response_time_ms=2000)

        assert updated_card.total_reviews == 1
        assert updated_card.correct_reviews == 1
        assert updated_card.repetitions >= 0
        assert updated_card.last_review is not None

    def test_process_review_incorrect(self):
        """Test processing incorrect review."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        updated_card = sm2.process_review(card, correct=False, response_time_ms=5000)

        assert updated_card.total_reviews == 1
        assert updated_card.correct_reviews == 0
        assert updated_card.repetitions == 0  # Reset

    def test_process_review_with_difficulty(self):
        """Test processing review with difficulty rating."""
        sm2 = SM2Algorithm()
        card = SM2Card(
            item_id="test_1",
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        updated_card = sm2.process_review(
            card,
            correct=True,
            response_time_ms=2000,
            difficulty_felt=2  # Easy
        )

        assert updated_card.total_reviews == 1

    # ========================================================================
    # Quality Score Calculation Tests
    # ========================================================================

    def test_quality_score_incorrect_slow(self):
        """Test quality score for incorrect slow answer."""
        sm2 = SM2Algorithm()
        quality = sm2._calculate_quality_score(
            correct=False,
            response_time_ms=20000,  # Very slow
            difficulty_felt=None
        )

        assert quality <= 2  # Should be 0-2

    def test_quality_score_correct_fast(self):
        """Test quality score for correct fast answer."""
        sm2 = SM2Algorithm()
        quality = sm2._calculate_quality_score(
            correct=True,
            response_time_ms=2000,  # Fast
            difficulty_felt=None
        )

        assert quality >= 4  # Should be 4-5

    def test_quality_score_correct_slow(self):
        """Test quality score for correct slow answer."""
        sm2 = SM2Algorithm()
        quality = sm2._calculate_quality_score(
            correct=True,
            response_time_ms=10000,  # Slow
            difficulty_felt=None
        )

        assert 3 <= quality <= 4

    # ========================================================================
    # Due Cards Tests
    # ========================================================================

    def test_get_due_cards_empty(self):
        """Test getting due cards from empty list."""
        sm2 = SM2Algorithm()
        due_cards = sm2.get_due_cards([])

        assert len(due_cards) == 0

    def test_get_due_cards_all_due(self):
        """Test getting due cards when all are due."""
        sm2 = SM2Algorithm()
        cards = [
            SM2Card(
                item_id=f"test_{i}",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                next_review=datetime.now() - timedelta(days=1)
            )
            for i in range(5)
        ]

        due_cards = sm2.get_due_cards(cards)

        assert len(due_cards) == 5

    def test_get_due_cards_none_due(self):
        """Test getting due cards when none are due."""
        sm2 = SM2Algorithm()
        cards = [
            SM2Card(
                item_id=f"test_{i}",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                next_review=datetime.now() + timedelta(days=1)
            )
            for i in range(5)
        ]

        due_cards = sm2.get_due_cards(cards)

        assert len(due_cards) == 0

    def test_get_due_cards_with_limit(self):
        """Test getting due cards with limit."""
        sm2 = SM2Algorithm()
        cards = [
            SM2Card(
                item_id=f"test_{i}",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                next_review=datetime.now() - timedelta(days=1)
            )
            for i in range(10)
        ]

        due_cards = sm2.get_due_cards(cards, count=5)

        assert len(due_cards) == 5

    def test_get_due_cards_sorted(self):
        """Test due cards are sorted by next_review."""
        sm2 = SM2Algorithm()
        cards = [
            SM2Card(
                item_id="test_1",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                next_review=datetime.now() - timedelta(days=3)
            ),
            SM2Card(
                item_id="test_2",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                next_review=datetime.now() - timedelta(days=1)
            ),
            SM2Card(
                item_id="test_3",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                next_review=datetime.now() - timedelta(days=5)
            )
        ]

        due_cards = sm2.get_due_cards(cards)

        # Should be sorted oldest first
        assert due_cards[0].item_id == "test_3"  # 5 days ago
        assert due_cards[-1].item_id == "test_2"  # 1 day ago


@pytest.mark.unit
@pytest.mark.learning
class TestAdaptiveDifficultyManager:
    """Test suite for AdaptiveDifficultyManager."""

    def test_manager_initialization(self):
        """Test manager initializes correctly."""
        manager = AdaptiveDifficultyManager()

        assert manager.difficulty == "intermediate"
        assert len(manager.recent_results) == 0

    def test_record_result(self):
        """Test recording exercise result."""
        manager = AdaptiveDifficultyManager()

        new_difficulty = manager.record_result(correct=True, response_time_ms=3000)

        assert len(manager.recent_results) == 1
        assert manager.recent_results[0] is True

    def test_difficulty_increase_on_high_performance(self):
        """Test difficulty increases with high performance."""
        manager = AdaptiveDifficultyManager(adjustment_threshold=5)

        # Record excellent performance
        for _ in range(5):
            manager.record_result(correct=True, response_time_ms=2000)

        assert manager.difficulty == "advanced"

    def test_difficulty_decrease_on_poor_performance(self):
        """Test difficulty decreases with poor performance."""
        manager = AdaptiveDifficultyManager(
            initial_difficulty="advanced",
            adjustment_threshold=5
        )

        # Record poor performance
        for _ in range(5):
            manager.record_result(correct=False, response_time_ms=10000)

        assert manager.difficulty == "intermediate"

    def test_difficulty_stays_same(self):
        """Test difficulty stays same with moderate performance."""
        manager = AdaptiveDifficultyManager(adjustment_threshold=5)

        # Record moderate performance
        for i in range(5):
            manager.record_result(
                correct=(i % 2 == 0),
                response_time_ms=5000
            )

        assert manager.difficulty == "intermediate"

    def test_get_performance_metrics(self):
        """Test getting performance metrics."""
        manager = AdaptiveDifficultyManager()

        for i in range(10):
            manager.record_result(
                correct=(i % 2 == 0),
                response_time_ms=3000 + i * 100
            )

        metrics = manager.get_performance_metrics()

        assert "accuracy" in metrics
        assert "average_time_ms" in metrics
        assert "sample_size" in metrics
        assert metrics["sample_size"] == 10


@pytest.mark.unit
@pytest.mark.learning
class TestLearningAlgorithm:
    """Test suite for main LearningAlgorithm class."""

    def test_algorithm_initialization(self, learning_algorithm):
        """Test algorithm initializes correctly."""
        assert learning_algorithm.sm2 is not None
        assert learning_algorithm.difficulty_manager is not None
        assert len(learning_algorithm.cards) == 0

    # ========================================================================
    # Card Management Tests
    # ========================================================================

    def test_add_card(self, learning_algorithm):
        """Test adding new card."""
        card = learning_algorithm.add_card("hablar", "present_subjunctive", "yo")

        assert isinstance(card, SM2Card)
        assert card.verb == "hablar"
        assert card.item_id in learning_algorithm.cards

    def test_add_duplicate_card(self, learning_algorithm):
        """Test adding duplicate card returns existing."""
        card1 = learning_algorithm.add_card("hablar", "present_subjunctive", "yo")
        card2 = learning_algorithm.add_card("hablar", "present_subjunctive", "yo")

        assert card1.item_id == card2.item_id
        assert len(learning_algorithm.cards) == 1

    # ========================================================================
    # Exercise Result Processing Tests
    # ========================================================================

    def test_process_exercise_result(self, learning_algorithm):
        """Test processing exercise result."""
        result = learning_algorithm.process_exercise_result(
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            correct=True,
            response_time_ms=2500
        )

        assert "card_updated" in result
        assert "difficulty_changed" in result
        assert "next_review" in result

    def test_process_creates_card_if_not_exists(self, learning_algorithm):
        """Test processing creates card if it doesn't exist."""
        assert len(learning_algorithm.cards) == 0

        learning_algorithm.process_exercise_result(
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            correct=True,
            response_time_ms=2500
        )

        assert len(learning_algorithm.cards) == 1

    # ========================================================================
    # Next Items Tests
    # ========================================================================

    def test_get_next_items_empty(self, learning_algorithm):
        """Test getting next items when empty."""
        items = learning_algorithm.get_next_items(count=10)

        assert len(items) == 0

    def test_get_next_items_prioritizes_due(self, learning_algorithm):
        """Test next items prioritizes due cards."""
        # Add some cards
        for i in range(5):
            learning_algorithm.add_card(f"verb{i}", "present_subjunctive", "yo")

        # Make some due
        for card in list(learning_algorithm.cards.values())[:3]:
            card.next_review = datetime.now() - timedelta(days=1)

        items = learning_algorithm.get_next_items(count=10)

        # Should prioritize the 3 due cards
        assert len(items) >= 3

    # ========================================================================
    # Statistics Tests
    # ========================================================================

    def test_get_statistics_empty(self, learning_algorithm):
        """Test statistics when no cards."""
        stats = learning_algorithm.get_statistics()

        assert stats["total_cards"] == 0
        assert stats["mastered_cards"] == 0
        assert stats["learning_cards"] == 0
        assert stats["new_cards"] == 0

    def test_get_statistics_with_cards(self, learning_algorithm):
        """Test statistics with cards."""
        # Add cards with different states
        card1 = learning_algorithm.add_card("hablar", "present_subjunctive", "yo")
        # Card is new by default (total_reviews = 0, repetitions = 0)

        card2 = learning_algorithm.add_card("comer", "present_subjunctive", "yo")
        card2.total_reviews = 2  # Has reviews
        card2.repetitions = 3  # Learning (< 5)

        card3 = learning_algorithm.add_card("vivir", "present_subjunctive", "yo")
        card3.total_reviews = 10  # Has reviews
        card3.repetitions = 6  # Mastered (>= 5)

        stats = learning_algorithm.get_statistics()

        assert stats["total_cards"] == 3
        assert stats["new_cards"] == 1
        # At least 1 learning and 1 mastered, total should be 3
        assert stats["learning_cards"] >= 1
        assert stats["mastered_cards"] >= 1

    def test_get_statistics_accuracy(self, learning_algorithm):
        """Test overall accuracy calculation."""
        card = learning_algorithm.add_card("hablar", "present_subjunctive", "yo")
        card.total_reviews = 10
        card.correct_reviews = 8

        stats = learning_algorithm.get_statistics()

        assert stats["overall_accuracy"] == 80.0

    # ========================================================================
    # Integration Tests
    # ========================================================================

    def test_full_learning_cycle(self, learning_algorithm):
        """Test complete learning cycle."""
        # First review
        result1 = learning_algorithm.process_exercise_result(
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            correct=True,
            response_time_ms=2000
        )

        assert result1["card_updated"]["repetitions"] >= 0

        # Second review (should have increased interval)
        result2 = learning_algorithm.process_exercise_result(
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            correct=True,
            response_time_ms=1500
        )

        assert result2["interval_days"] >= result1["interval_days"]
