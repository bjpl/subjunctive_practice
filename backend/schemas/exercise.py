"""
Pydantic schemas for exercise-related models.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from backend.models.exercise import VerbType, SubjunctiveTense, ExerciseType, DifficultyLevel


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
    explanation: Optional[str] = None
    trigger_phrase: Optional[str] = None
    hint: Optional[str] = None


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
    recommended_level: Optional[str] = Field(None, regex=r"^[ABC][12]$")


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


class AnswerValidation(BaseModel):
    """Schema for answer validation response."""
    is_correct: bool
    correct_answer: str
    user_answer: str
    feedback: str
    explanation: Optional[str] = None
    score: int = Field(..., ge=0, le=100)
    alternative_answers: Optional[List[str]] = Field(default_factory=list)


class ExerciseListResponse(BaseModel):
    """Schema for paginated exercise list."""
    exercises: List[ExerciseResponse]
    total: int
    page: int = 1
    page_size: int = 10
    has_more: bool = False
