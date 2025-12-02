"""
Pydantic schemas for exercise-related models.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from models.exercise import VerbType, SubjunctiveTense, ExerciseType, DifficultyLevel


class VerbBase(BaseModel):
    """Base verb schema."""
    infinitive: str = Field(..., max_length=50)
    english_translation: str = Field(..., max_length=100)
    verb_type: VerbType


class VerbCreate(VerbBase):
    """Schema for creating a verb."""
    present_subjunctive: Dict[str, str]
    imperfect_subjunctive_ra: Optional[Dict[str, str]] = None
    imperfect_subjunctive_se: Optional[Dict[str, str]] = None
    frequency_rank: Optional[int] = None
    is_irregular: bool = False
    irregularity_notes: Optional[str] = None


class VerbResponse(VerbBase):
    """Schema for verb response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    present_subjunctive: Dict[str, str]
    imperfect_subjunctive_ra: Optional[Dict[str, str]] = None
    imperfect_subjunctive_se: Optional[Dict[str, str]] = None
    frequency_rank: Optional[int] = None
    is_irregular: bool
    irregularity_notes: Optional[str] = None
    created_at: datetime


class ExerciseBase(BaseModel):
    """Base exercise schema."""
    exercise_type: ExerciseType
    tense: SubjunctiveTense
    difficulty: DifficultyLevel
    prompt: str
    person: Optional[str] = None  # Grammatical person: "yo", "tú", "él/ella/usted", etc.
    explanation: Optional[str] = None
    trigger_phrase: Optional[str] = None
    hint: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ExerciseCreate(ExerciseBase):
    """Schema for creating an exercise."""
    verb_id: int
    correct_answer: str
    alternative_answers: Optional[List[str]] = None
    distractors: Optional[List[str]] = None


class ExerciseResponse(ExerciseBase):
    """Schema for exercise response (public - no answers shown)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    verb_id: int
    verb: Optional[VerbResponse] = None
    distractors: Optional[List[str]] = None  # For multiple choice
    is_active: bool
    usage_count: int
    success_rate: int
    tags: Optional[List[str]] = Field(default_factory=list)


class ExerciseWithAnswer(ExerciseResponse):
    """Schema for exercise with answer (for review/admin)."""
    correct_answer: str
    alternative_answers: Optional[List[str]] = None


class ScenarioBase(BaseModel):
    """Base scenario schema."""
    title: str = Field(..., max_length=100)
    description: str
    theme: str = Field(..., max_length=50)
    context: Optional[str] = None
    image_url: Optional[str] = None
    recommended_level: Optional[str] = Field(None, pattern=r"^[ABC][12]$")


class ScenarioCreate(ScenarioBase):
    """Schema for creating a scenario."""
    pass


class ScenarioResponse(ScenarioBase):
    """Schema for scenario response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    exercise_count: Optional[int] = None


class ScenarioWithExercises(ScenarioResponse):
    """Schema for scenario with exercises."""
    exercises: List[ExerciseResponse] = []


# ==================== Answer Submission & Validation ====================

class AnswerSubmit(BaseModel):
    """Schema for submitting an exercise answer."""
    exercise_id: str
    user_answer: str = Field(..., min_length=1, max_length=200)
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")

    # Session management
    session_id: Optional[int] = Field(None, description="Session ID to associate this attempt with")

    # Optional fields for custom exercise metadata (generated exercises with ID starting with "gen_")
    verb: Optional[str] = Field(None, description="Verb infinitive for custom exercises")
    tense: Optional[str] = Field(None, description="Subjunctive tense for custom exercises")
    person: Optional[str] = Field(None, description="Grammatical person for custom exercises")
    correct_answer: Optional[str] = Field(None, description="Expected correct answer for custom exercises")
    alternative_answers: Optional[List[str]] = Field(None, description="Alternative acceptable answers for custom exercises")
    explanation: Optional[str] = Field(None, description="Exercise explanation for custom exercises")
    trigger_phrase: Optional[str] = Field(None, description="WEIRDO trigger phrase for custom exercises")


class AnswerValidation(BaseModel):
    """Schema for answer validation response."""
    is_correct: bool
    correct_answer: str
    user_answer: str
    feedback: str
    explanation: Optional[str] = None
    score: int = Field(..., ge=0, le=100)
    alternative_answers: Optional[List[str]] = Field(default_factory=list)

    # Enhanced feedback from learning services
    error_type: Optional[str] = None
    suggestions: Optional[List[str]] = Field(default_factory=list)
    related_rules: Optional[List[str]] = Field(default_factory=list)
    encouragement: Optional[str] = None
    next_steps: Optional[List[str]] = Field(default_factory=list)

    # Spaced repetition data
    next_review_date: Optional[str] = None
    interval_days: Optional[int] = None
    difficulty_level: Optional[str] = None


class ExerciseListResponse(BaseModel):
    """Schema for paginated exercise list."""
    exercises: List[ExerciseResponse]
    total: int
    page: int = 1
    page_size: int = 10
    has_more: bool = False


# ==================== Session Management ====================

class SessionStartRequest(BaseModel):
    """Schema for starting a new practice session."""
    session_type: str = Field(default="practice", description="Type of session: practice, review, test")


class SessionStartResponse(BaseModel):
    """Schema for session start response."""
    session_id: int
    started_at: datetime


class SessionEndRequest(BaseModel):
    """Schema for ending a practice session."""
    session_id: int


class SessionEndResponse(BaseModel):
    """Schema for session end response with summary stats."""
    session_id: int
    started_at: datetime
    ended_at: datetime
    duration_seconds: int
    total_exercises: int
    correct_answers: int
    score_percentage: float
    session_type: str


# ==================== Spaced Repetition / Review ====================

class DueReviewItem(BaseModel):
    """Schema for a single review item that is due."""
    model_config = ConfigDict(from_attributes=True)

    verb_id: int
    verb_infinitive: str
    verb_translation: str
    tense: str
    person: Optional[str] = None
    days_overdue: int
    difficulty_level: str  # "new", "learning", "reviewing", "mastered"
    easiness_factor: float
    next_review_date: datetime
    review_count: int
    success_rate: float  # 0-100%


class DueReviewResponse(BaseModel):
    """Schema for response containing due review items."""
    items: List[DueReviewItem]
    total_due: int
    next_review_date: Optional[datetime] = None


class ReviewStatsResponse(BaseModel):
    """Schema for review statistics."""
    total_due: int
    due_by_difficulty: Dict[str, int]  # {"new": 5, "learning": 10, ...}
    average_retention: float  # 0-100%
    total_reviewed: int
    reviews_today: int
    streak_days: int
