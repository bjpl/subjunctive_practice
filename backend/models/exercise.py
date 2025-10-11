"""
Exercise content models: Verbs, Exercises, and Scenarios.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base


class VerbType(str, enum.Enum):
    """Spanish verb types."""
    REGULAR = "regular"
    IRREGULAR = "irregular"
    STEM_CHANGING = "stem_changing"
    REFLEXIVE = "reflexive"


class SubjunctiveTense(str, enum.Enum):
    """Subjunctive tense types."""
    PRESENT = "present_subjunctive"
    IMPERFECT = "imperfect_subjunctive"
    PRESENT_PERFECT = "present_perfect_subjunctive"
    PLUPERFECT = "pluperfect_subjunctive"


class ExerciseType(str, enum.Enum):
    """Exercise format types."""
    FILL_BLANK = "fill_blank"
    MULTIPLE_CHOICE = "multiple_choice"
    CONJUGATION = "conjugation"
    TRANSLATION = "translation"
    TRIGGER_IDENTIFICATION = "trigger_identification"


class DifficultyLevel(int, enum.Enum):
    """Exercise difficulty levels."""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


class Verb(Base):
    """
    Spanish verb model with conjugation data.
    """
    __tablename__ = "verbs"

    id = Column(Integer, primary_key=True, index=True)
    infinitive = Column(String(50), unique=True, nullable=False, index=True)
    english_translation = Column(String(100), nullable=False)
    verb_type = Column(SQLEnum(VerbType), nullable=False, index=True)

    # Conjugation data (stored as JSON)
    present_subjunctive = Column(JSON, nullable=False)  # {yo: "hable", tú: "hables", ...}
    imperfect_subjunctive_ra = Column(JSON, nullable=True)  # {yo: "hablara", ...}
    imperfect_subjunctive_se = Column(JSON, nullable=True)  # {yo: "hablase", ...}

    # Metadata
    frequency_rank = Column(Integer, nullable=True)  # 1-1000, lower = more common
    is_irregular = Column(Boolean, default=False, nullable=False)
    irregularity_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    exercises = relationship("Exercise", back_populates="verb", cascade="all, delete-orphan")
    review_schedules = relationship("ReviewSchedule", back_populates="verb")

    def __repr__(self):
        return f"<Verb(id={self.id}, infinitive='{self.infinitive}', type={self.verb_type})>"


class Exercise(Base):
    """
    Exercise model with prompts and answers.
    """
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    verb_id = Column(Integer, ForeignKey("verbs.id", ondelete="CASCADE"), nullable=False, index=True)

    # Exercise content
    exercise_type = Column(SQLEnum(ExerciseType), nullable=False, index=True)
    tense = Column(SQLEnum(SubjunctiveTense), nullable=False, index=True)
    difficulty = Column(SQLEnum(DifficultyLevel), nullable=False, index=True)

    prompt = Column(Text, nullable=False)
    correct_answer = Column(String(200), nullable=False)
    alternative_answers = Column(JSON, nullable=True)  # ["fuese", "fuera"]

    # For multiple choice
    distractors = Column(JSON, nullable=True)  # ["hablo", "hablé", "hablaré"]

    # Learning support
    explanation = Column(Text, nullable=True)
    trigger_phrase = Column(String(100), nullable=True)  # "espero que", "no creo que"
    hint = Column(Text, nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    usage_count = Column(Integer, default=0, nullable=False)
    success_rate = Column(Integer, default=0, nullable=False)  # 0-100%

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    verb = relationship("Verb", back_populates="exercises")
    scenarios = relationship("ExerciseScenario", back_populates="exercise", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="exercise")

    def __repr__(self):
        return f"<Exercise(id={self.id}, type={self.exercise_type}, difficulty={self.difficulty})>"


class Scenario(Base):
    """
    Contextual scenarios for exercises.
    Groups exercises around real-world themes.
    """
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    # Scenario metadata
    theme = Column(String(50), nullable=False)  # "travel", "work", "relationships"
    context = Column(Text, nullable=True)  # Additional context/story
    image_url = Column(String(500), nullable=True)

    # Learning metadata
    recommended_level = Column(String(2), nullable=True)  # "A1", "B2", etc.

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    exercises = relationship("ExerciseScenario", back_populates="scenario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scenario(id={self.id}, title='{self.title}', theme='{self.theme}')>"


class ExerciseScenario(Base):
    """
    Many-to-many relationship between Exercise and Scenario.
    Allows exercises to be used in multiple scenarios.
    """
    __tablename__ = "exercise_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id", ondelete="CASCADE"), nullable=False, index=True)

    # Ordering within scenario
    order_index = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    exercise = relationship("Exercise", back_populates="scenarios")
    scenario = relationship("Scenario", back_populates="exercises")

    def __repr__(self):
        return f"<ExerciseScenario(exercise_id={self.exercise_id}, scenario_id={self.scenario_id})>"
